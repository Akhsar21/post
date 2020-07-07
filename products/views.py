import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from django.utils.translation import gettext as _
from django.contrib import messages
from django.http import HttpResponse
from django.views.generic import CreateView
from django.shortcuts import render, redirect, reverse
from .forms import PurchaseForm
from .models import Product, Purchase
from .utils import get_simple_plot, get_salesman_from_id, get_image
# Create your views here.

def sales_dist_view(request):
    df = pd.DataFrame(Purchase.objects.all().values())
    df['salesman_id'] = df['salesman_id'].apply(get_salesman_from_id)
    df.rename({'salesman_id':'salesman'}, axis=1, inplace=True)
    df['date'] = df['date'].apply(lambda x: x.strftime('%Y-%m-%d'))
    
    plt.switch_backend('Agg')
    plt.xticks(rotation=45)
    sns.barplot(x='date', y='total_price', hue='salesman', data=df)
    plt.tight_layout()
    graph = get_image()

    # return HttpResponse("Hello")
    return render(request, 'products/sales.html', {'graph': graph})


def chart_select_view(request):
    graph = None
    error_message = None
    df = None
    price = None

    try:
        product_df = pd.DataFrame(Product.objects.all().values())
        purchase_df = pd.DataFrame(Purchase.objects.all().values())
        product_df['product_id'] = product_df['id']
    
        if purchase_df.shape[0] > 0:
            df = pd.merge(purchase_df, product_df, on='product_id').drop(['id_y', 'date_y'], axis=1).rename({'id_x': 'id', 'date_x': 'date'}, axis=1)
            price = df['price']

            if request.method == 'POST':
                chart_type = request.POST.get('sales')
                date_from = request.POST['date_from']
                date_to = request.POST['date_to']

                df['date'] = df['date'].apply(lambda x: x.strftime('%Y-%m-%d'))
                df2 = df.groupby('date', as_index=False)['total_price'].agg('sum')

                if chart_type != "":
                    if date_from != "" and date_to != "":
                        df = df[(df['date'] > date_from) & (df['date'] < date_to)]
                        df2 = df.groupby('date', as_index=False)[
                            'total_price'].agg('sum')
                    # function to get a graph
                    graph = get_simple_plot(
                        chart_type, x=df2['date'], y=df2['total_price'], data=df)
                else:
                    messages.error(request, _(
                        "Please select a chart type to continue"))

        else:
            messages.error(request, _("No records in the database"))
            error_message = 'No records in the database'

    except:
        product_df = None
        purchase_df = None
        messages.error(request, _("No records in the database"))
        error_message = 'No records in the database'

    context = {
        'graph': graph,
        'price': price,
        'error_message': error_message,
    }
    return render(request, 'products/main.html', context)


class PurchaseCreateView(CreateView):
    model = Purchase
    form_class = PurchaseForm

    def form_valid(self, form):
        form.instance.salesman = self.request.user
        form.save()
        messages.success(self.request, _("The purchase has been added"))
        return redirect(reverse("add-purchase-view"))
