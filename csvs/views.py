from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth.models import User
# from django.utils.translation import gettext as _
from django.views.generic import CreateView
from .forms import CsvForm
from .models import Csv
from products.models import Product, Purchase
import csv

# Create your views here.


def upload_file_view(request):
    form = CsvForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        form = CsvForm()

        try:
            obj = Csv.objects.get(activated=False)
            with open(obj.file_name.path, 'r') as f:
                reader = csv.reader(f)

                for row in reader:
                    print(row)
                    row = "".join(row)
                    row = row.replace(";", " ")
                    row = row.split()
                    user = User.objects.get(id=row[3])
                    prod, _ = Product.objects.get_or_create(name=row[0])
                    Purchase.objects.create(
                        product=prod,
                        price=int(row[2]),
                        quantity=int(row[1]),
                        salesman=user,
                        date=row[4]
                    )

            obj.activated = True
            obj.save()
            messages.success(request, "Upload Successfully!")
        except:
            messages.error(request, "Ups, Something went wrong...")

    return render(request, 'csvs/upload.html', {'form': form})
