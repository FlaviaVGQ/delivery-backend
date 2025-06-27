from io import BytesIO
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.contrib.auth.models import User
from rest_framework import status
from orders.models import OrderList
from save_company_info.models import NewCompanyInfo
from product.models import Product
from datetime import datetime

from reportlab.lib.utils import ImageReader
from django.conf import settings
import os


class OrderReportPDFView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response({"error": "Parâmetro user_id é obrigatório."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "Usuário não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        try:
            company = NewCompanyInfo.objects.get(user=user)
        except NewCompanyInfo.DoesNotExist:
            company = None

        orders = OrderList.objects.filter(user_id=user_id)

        all_items = []
        for order in orders:
            for item in order.items.all():
                try:
                    product_obj = Product.objects.get(name=item.product_name)
                    category_name = product_obj.category.name if product_obj.category else 'Sem categoria'
                except Product.DoesNotExist:
                    category_name = 'Sem categoria'

                all_items.append({
                    'product_name': item.product_name,
                    'price': item.price,
                    'quantity': item.quantity,
                    'category': category_name,
                })

        total_vendas = sum(item['price'] * item['quantity'] for item in all_items)
        total_itens = sum(item['quantity'] for item in all_items)
        categorias = set(item['category'] for item in all_items)
        total_categorias = len(categorias)

        produtos_por_categoria = {}
        for item in all_items:
            cat = item['category']
            produtos_por_categoria[cat] = produtos_por_categoria.get(cat, 0) + item['quantity']

        ultimos_pedidos = orders.order_by('-id')[:5]

        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4

        y = height - 50
        box_height = 90
        box_padding = 10
        box_width = width - 100

        data_hora = datetime.now().strftime('%d/%m/%Y %H:%M')
        p.setFont("Helvetica", 10)
        p.drawRightString(width - 50, y + 10, data_hora)
        p.setLineWidth(1)
        p.roundRect(50, y - box_height, box_width, box_height, radius=10, stroke=1, fill=0)
        text_x = 60
        text_y = y - box_padding - 15

        if company:
            p.setFont("Helvetica-Bold", 16)
            p.drawString(text_x, text_y, company.name)
            text_y -= 20

            if company.image:
                logo_path = os.path.join(settings.MEDIA_ROOT, company.image.name)
                if os.path.exists(logo_path):
                    try:
                        logo = ImageReader(logo_path)
                        logo_width = 125
                        logo_height = 50
                        p.drawImage(
                            logo,
                            60 + box_width - logo_width - 10,
                            y - box_padding - logo_height,
                            width=logo_width,
                            height=logo_height,
                            preserveAspectRatio=True,
                        )
                    except Exception as e:
                        print(f"Erro ao carregar logo: {e}")

            p.setFont("Helvetica", 10)
            if company.address:
                p.drawString(text_x, text_y, f"Endereço: {company.address}")
                text_y -= 15
            if company.contact:
                p.drawString(text_x, text_y, f"Contato: {company.contact}")
                text_y -= 15
            if company.opening_hours:
                p.drawString(text_x, text_y, f"Horário: {company.opening_hours}")
                text_y -= 15



        p.line(50, y - box_height - 10, 50 + box_width, y - box_height - 10)
        y = y - box_height - 30
        p.setFont("Helvetica-Bold", 16)
        p.drawCentredString(width / 2, y, "Relatório")
        y -= 40
        p.setFont("Helvetica-Bold", 12)
        p.drawString(50, y, "Resumo:")
        y -= 20
        p.setFont("Helvetica", 12)
        p.drawString(60, y, f"Total de Vendas: R$ {total_vendas:.2f}")
        y -= 15
        p.drawString(60, y, f"Total de Itens Vendidos: {total_itens}")
        y -= 15
        p.drawString(60, y, f"Total de Categorias: {total_categorias}")
        y -= 30
        p.setFont("Helvetica-Bold", 12)
        p.drawString(50, y, "Produtos por Categoria (quantidade):")
        y -= 20
        p.setFont("Helvetica", 12)
        for cat, qty in produtos_por_categoria.items():
            p.drawString(60, y, f"{cat}: {qty}")
            y -= 15
            if y < 100:
                p.showPage()
                y = height - 50

        y -= 20

        p.setFont("Helvetica-Bold", 12)
        p.drawString(50, y, "Últimos Pedidos:")
        y -= 25

        p.setFont("Helvetica-Bold", 10)
        headers = ["Cliente", "Obs.", "Itens", "Valor Total", "Pagamento", "Status"]
        col_x = [50, 115, 240, 370, 450, 520]
        for i, header in enumerate(headers):
            p.drawString(col_x[i], y, header)
        y -= 15
        p.line(50, y + 5, 550, y + 5)
        y -= 20

        p.setFont("Helvetica", 10)

        for order in ultimos_pedidos:
            if y < 70:
                p.showPage()
                y = height - 50

            itens_text = ', '.join(
                [f"{item.product_name} ({item.quantity})" for item in order.items.all()]
            )
            p.drawString(col_x[0], y, order.customer_name or "---")
            p.drawString(col_x[1], y, (order.observation or "---")[:20])
            p.drawString(col_x[2], y, itens_text[:40])
            p.drawString(col_x[3], y, f"R$ {float(order.total_price or 0):.2f}")
            p.drawString(col_x[4], y, order.payment_method or "---")
            p.drawString(col_x[5], y, order.status or "---")
            y -= 15

        p.showPage()
        p.save()

        buffer.seek(0)
        response = HttpResponse(buffer, content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename=relatorio.pdf'
        return response
