# -*- coding: utf-8 -*-
# Copyright (c) 2014 Polytechnique.org
# This software is distributed under the GPLv3+ license.


import datetime

from django.utils import timezone

import factory
import factory.django
import factory.fuzzy

from django_factory_boy import auth as auth_factories

from . import models

class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Product

    kind = factory.Iterator([c[0] for c in models.Product.KIND_CHOICES])
    name = factory.Sequence(lambda n: "Product #%s" % n)


class ProductPriceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.ProductPrice

    product = factory.SubFactory(ProductFactory)
    amount = factory.fuzzy.FuzzyInteger(100, 10000, step=50)
    available_since = factory.LazyAttribute(lambda _o: timezone.now())
    available_until = factory.LazyAttribute(lambda o: o.available_since + datetime.timedelta(days=365))


class PaymentModeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.PaymentMode

    owner = factory.SubFactory(auth_factories.UserF)
    kind = factory.Iterator([c[0] for c in models.PaymentMode.KIND_CHOICES])
    reference = factory.Sequence(lambda n: "42-42-%12d" % n)


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Order

    payment_mode = factory.SubFactory(PaymentModeFactory)
    payment_date = factory.LazyAttribute(lambda _o: timezone.now())
    amount = factory.fuzzy.FuzzyInteger(100, 10000, step=50)


class OrderItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.OrderItem

    user = factory.SubFactory(auth_factories.UserF)
    product_price = models.SubFactory(ProductPriceFactory)
    order = models.SubFactory(OrderFactory,
        # Forward '.user' to the order.payment_mode.owner
        payment_mode__owner=factory.SelfAttribute('...user'),
    )

    billing_date = factory.LazyAttribute(lambda _o: timezone.now().date())
