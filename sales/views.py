from django.utils.timezone import now
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Sale,Customer,Invoice
from .serializers import SaleSerializer,CustomerSerializer
from django.http import HttpResponse
from django.views import View
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from .models import Invoice
from .serializers import InvoiceSerializer, SaleSerializer
from customers.models import ServiceRecord,Vehicle
from services.models import Service
from datetime import date
import io,os
from datetime import datetime
from django.db.models import Sum
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.conf import settings
from reportlab.platypus import Image
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.graphics.shapes import Drawing, Line


class TaxReportPDFView(APIView):
    def get(self, request):
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")

        if not start_date or not end_date:
            return JsonResponse({"error": "Please provide start_date and end_date in YYYY-MM-DD format."}, status=400)

        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        except ValueError:
            return JsonResponse({"error": "Invalid date format. Use YYYY-MM-DD."}, status=400)

        sales = Sale.objects.filter(date__range=[start_date, end_date])
        total_sales = sales.aggregate(Sum("amount"))['amount__sum'] or 0.00
        total_tax = sales.aggregate(Sum("tax_amount"))['tax_amount__sum'] or 0.00
        total_overall = sales.aggregate(Sum("total_amount"))['total_amount__sum'] or 0.00

        # Create PDF buffer
        buffer = io.BytesIO()
        pdf = SimpleDocTemplate(buffer, pagesize=A4)
        elements = []
        styles = getSampleStyleSheet()

        # **Header: Logo and Title**
        logo_path = os.path.join(settings.MEDIA_ROOT, "cleanbay-nbg.png")
        if os.path.exists(logo_path):
            logo = Image(logo_path, width=120, height=50)
            elements.append(logo)

        elements.append(Spacer(1, 0.2 * inch))

        # **Company Title**
        elements.append(Paragraph("<b>CleanBay Tax Report</b>", styles["Title"]))
        elements.append(Paragraph(f"<b>Report Period:</b> {start_date} to {end_date}", styles["Normal"]))
        elements.append(Spacer(1, 0.3 * inch))

        # **Table Data**
        data = [["Date", "Service", "Customer", "Amount", "VAT Rate", "Tax Amount", "Total"]]
        total_amount = total_tax_amount = total_final_amount = 0

        for sale in sales:
            data.append([
                sale.date.strftime("%Y-%m-%d"),
                sale.service.name,
                sale.customer.name if sale.customer else "N/A",
                f"KES {sale.amount:,.2f}",
                f"{sale.tax_rate}%",
                f"KES {sale.tax_amount:,.2f}",
                f"KES {sale.total_amount:,.2f}",
            ])
            total_amount += sale.amount
            total_tax_amount += sale.tax_amount
            total_final_amount += sale.total_amount

        # **Totals Row**
        data.append([
            "", "", "Total:", f"KES {total_amount:,.2f}", "", f"KES {total_tax_amount:,.2f}",
            f"KES {total_final_amount:,.2f}"
        ])

        # **Table Formatting**
        table = Table(data, colWidths=[70, 100, 100, 80, 60, 80, 80])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (-1, -1), (-1, -1), colors.lightgrey),  # Total row background
            ('FONTNAME', (-1, -1), (-1, -1), 'Helvetica-Bold'),
        ]))

        elements.append(table)
        elements.append(Spacer(1, 0.5 * inch))

        # **Signature Section**
        elements.append(Spacer(1, 0.3 * inch))
        elements.append(Paragraph("<b>Authorized Signature</b>", styles["Normal"]))
        elements.append(Spacer(1, 0.2 * inch))
        line = Drawing(250, 1)
        line.add(Line(0, 0, 250, 0))  # Draw a horizontal line
        elements.append(line)

        elements.append(Spacer(1, 0.1 * inch))
        elements.append(Paragraph("Signed By: _______________________________________", styles["Normal"]))
        elements.append(Spacer(1, 0.1 * inch))
        elements.append(Paragraph(f"Date: {datetime.now().strftime('%Y-%m-%d')}", styles["Normal"]))

        # **Footer**
        elements.append(Spacer(1, 0.5 * inch))
        elements.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles["Italic"]))

        # **Build PDF**
        pdf.build(elements)

        # **Save File**
        buffer.seek(0)
        filename = f"tax_report_{start_date}_to_{end_date}.pdf"
        file_path = os.path.join(settings.MEDIA_ROOT, filename)
        os.makedirs(settings.MEDIA_ROOT, exist_ok=True)

        with default_storage.open(file_path, 'wb') as f:
            f.write(buffer.getvalue())

        pdf_url = request.build_absolute_uri(settings.MEDIA_URL + filename)
        return JsonResponse({"pdf_url": pdf_url})


class InvoicePDFView(View):
    def get(self, request, invoice_id, *args, **kwargs):
        try:
            invoice = Invoice.objects.get(id=invoice_id)
        except Invoice.DoesNotExist:
            return HttpResponse("Invoice not found", status=404)

        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = f'inline; filename="{invoice.invoice_number}.pdf"'

        pdf = canvas.Canvas(response, pagesize=A4)
        width, height = A4
        y_position = height - 50

        # **Include Logo**
        logo_path = os.path.join(settings.MEDIA_ROOT, "cleanbay-nbg.png")  # Adjust filename if needed
        if os.path.exists(logo_path):
            pdf.drawImage(logo_path, 50, height - 100, width=120, height=60, preserveAspectRatio=True, mask='auto')
            y_position -= 70  # Adjust space after logo

        # **Centered INVOICE Heading**
        pdf.setFont("Helvetica-Bold", 18)
        pdf.drawCentredString(width / 2, y_position, "INVOICE")
        y_position -= 30

        # **Invoice Details**
        pdf.setFont("Helvetica", 12)
        pdf.drawString(400, y_position, f"Date Issued: {invoice.date_issued.strftime('%Y-%m-%d')}")
        y_position -= 20
        pdf.drawString(50, y_position, f"Status: {invoice.get_status_display()}")

        # **Customer Details**
        y_position -= 40
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(50, y_position, "Bill To:")
        pdf.setFont("Helvetica", 12)
        y_position -= 20

        if invoice.customer:
            pdf.drawString(50, y_position, f"Name: {invoice.customer.name}")
            y_position -= 20
            pdf.drawString(50, y_position, f"Phone: {invoice.customer.phone_number}")
            y_position -= 20
            pdf.drawString(50, y_position, f"Email: {invoice.customer.email}")
        else:
            pdf.drawString(50, y_position, "Customer: Walk-in Client")

        y_position -= 40

        # **Sales Table**
        sales_data = [["#", "Service/Product", "Quantity", "Unit Price (KES)", "Tax (KES)", "Total (KES)"]]
        total_price = 0
        total_tax = 0

        for idx, sale in enumerate(invoice.sales.all(), start=1):
            serialized_sale = SaleSerializer(sale).data
            unit_price = sale.amount
            tax_amount = sale.tax_amount
            total_sale = sale.total_amount
            total_price += unit_price
            total_tax += tax_amount

            sales_data.append([
                str(idx),
                serialized_sale['service_name'],
                "1",
                f"{unit_price:,.2f}",
                f"{tax_amount:,.2f}",
                f"{total_sale:,.2f}",
            ])

        table = Table(sales_data, colWidths=[30, 180, 60, 80, 80, 80])
        table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ])
        )

        table.wrapOn(pdf, width, height)
        table.drawOn(pdf, 50, y_position - (20 * len(sales_data)))

        # **Invoice Totals**
        serialized_invoice = InvoiceSerializer(invoice, context={"request": request}).data
        total_amount = serialized_invoice.get("total_amount", invoice.total_amount)
        total_paid = serialized_invoice.get("total_paid", invoice.total_paid)
        balance_due = total_amount - total_paid

        y_position -= (20 * (len(sales_data) + 2))
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(350, y_position, f"Subtotal: KES {total_price:,.2f}")
        y_position -= 20
        pdf.drawString(350, y_position, f"Tax: KES {total_tax:,.2f}")
        y_position -= 20
        pdf.drawString(350, y_position, f"Total Amount: KES {total_amount:,.2f}")
        y_position -= 20
        pdf.drawString(350, y_position, f"Amount Paid: KES {total_paid:,.2f}")
        y_position -= 20
        pdf.drawString(350, y_position, f"Balance Due: KES {balance_due:,.2f}")

        # **PAID Stamp**
        if balance_due == 0:
            pdf.setFillColor(colors.green)
            pdf.setFont("Helvetica-Bold", 20)
            pdf.drawString(250, 200, "PAID")

        # **Footer**
        pdf.setFont("Helvetica-Oblique", 10)
        pdf.setFillColor(colors.black)
        pdf.drawString(50, 50, "Thank you for your business!")

        # Finalize the PDF
        pdf.showPage()
        pdf.save()

        return response




class SalesListView(generics.ListCreateAPIView):
    queryset = Sale.objects.all().order_by('-date')
    serializer_class = SaleSerializer

    def list(self, request, *args, **kwargs):
        # Get the filter parameters from the request query
        day = request.query_params.get("day")
        month = request.query_params.get("month")
        year = request.query_params.get("year")

        # Apply filters to the queryset if they exist
        sales = Sale.objects.all()

        # Filter by year if provided
        if year:
            sales = sales.filter(date__year=year)

        # Filter by month if provided
        if month:
            sales = sales.filter(date__month=month)

        # Filter by day if provided
        if day:
            sales = sales.filter(date__day=day)

        # Serialize the filtered data
        serializer = SaleSerializer(sales, many=True)

        # Return custom response with the filtered data
        return Response({
            "data": serializer.data,
            "message": "Services retrieved successfully",
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        if request.data:
            try:
                vehicle = Vehicle.objects.get(pk=request.data.get('vehicle'))
                service = Service.objects.get(pk=request.data.get('service'))
            except Vehicle.DoesNotExist:
                return Response({"message": "Vehicle not found", "status": status.HTTP_404_NOT_FOUND},
                                status=status.HTTP_404_NOT_FOUND)
            except Service.DoesNotExist:
                return Response({"message": "Service not found", "status": status.HTTP_404_NOT_FOUND},
                                status=status.HTTP_404_NOT_FOUND)


            record_exists = ServiceRecord.objects.filter(
                service=service,
                vehicle=vehicle,
                date_added=date.today()  # Compare only the date
            ).exists()

            if record_exists:
                return Response({
                    "message": "Service record already exists for this vehicle and service",
                    "status": status.HTTP_400_BAD_REQUEST
                }, status=status.HTTP_400_BAD_REQUEST)


            ServiceRecord.objects.create(
                vehicle=vehicle,
                service=service,
                cost=request.data.get('amount'),
            )

            serializer = self.get_serializer(data=request.data)
            print("Creating ",request.data)
            if serializer.is_valid():
                serializer.save()

                return Response({
                    "data": serializer.data,
                    "message": "Sale created successfully",
                    "status": status.HTTP_201_CREATED
                }, status=status.HTTP_201_CREATED)

            return Response({
                "errors": serializer.errors,
                "message": "Failed to create sale",
                "status": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                "message": "Invalid request payload",
                "status": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_400_BAD_REQUEST)


class InvoiceListCreateView(generics.ListCreateAPIView):
    serializer_class = InvoiceSerializer

    def get_queryset(self):
        queryset = Invoice.objects.all()
        day = self.request.GET.get("day")
        month = self.request.GET.get("month")
        year = self.request.GET.get("year")

        if year:
            queryset = queryset.filter(date_issued__year=year)
        if month:
            queryset = queryset.filter(date_issued__month=month)
        if day:
            queryset = queryset.filter(date_issued__day=day)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True, context={"request": request})
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        sales_ids = request.data.get("sales_ids", [])  # Expecting a list of sale IDs

        if not sales_ids:
            return Response({
                "errors": {"sales_ids": ["This field is required."]},
                "message": "Invoice creation failed",
                "status": status.HTTP_400_BAD_REQUEST
            })

        # Check if any of the sales are already linked to an invoice
        existing_invoices = Sale.objects.filter(id__in=sales_ids, invoices__isnull=False).distinct()
        if existing_invoices.exists():
            return Response({
                "errors": {"sales_ids": ["One or more sales are already linked to an invoice."]},
                "message": "Invoice creation failed",
                "status": status.HTTP_400_BAD_REQUEST
            })

        # Get customer from the first sale
        customer = Sale.objects.get(pk=sales_ids[0]).customer
        request.data["customer"] = customer.id

        serializer = self.get_serializer(data=request.data)
        print("Creating ", serializer.initial_data)

        if serializer.is_valid():
            invoice = serializer.save()

            # Link sales to the invoice if provided
            sales = Sale.objects.filter(id__in=sales_ids)
            invoice.sales.set(sales)  # ✅ Correctly set ManyToMany relationships
            for sale in sales:
                sale.invoice = invoice
                sale.save()
            return Response({
                "data": serializer.data,
                "message": "Invoice created successfully",
                "status": status.HTTP_201_CREATED
            })

        return Response({
            "errors": serializer.errors,
            "message": "Invoice creation failed",
            "status": status.HTTP_400_BAD_REQUEST
        })


class InvoiceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

    def update(self, request, *args, **kwargs):
        """Handles updating an invoice and its linked sales."""
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        if serializer.is_valid():
            invoice = serializer.save()

            # If sales were provided, update them
            sales_data = request.data.get("sales", [])
            if sales_data:
                # Remove existing sales linked to this invoice
                instance.sales.clear()

                # Add new sales
                for sale_id in sales_data:
                    try:
                        sale = Sale.objects.get(id=sale_id)
                        sale.invoice = invoice
                        sale.save()
                    except Sale.DoesNotExist:
                        return Response(
                            {"message": f"Sale ID {sale_id} not found"},
                            status=status.HTTP_400_BAD_REQUEST
                        )

            return Response({
                "data": serializer.data,
                "message": "Invoice updated successfully",
                "status": status.HTTP_200_OK
            })

        return Response({
            "errors": serializer.errors,
            "message": "Invoice update failed",
            "status": status.HTTP_400_BAD_REQUEST
        })


