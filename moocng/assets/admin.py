# Copyright 2013 Rooter Analysis S.L.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.contrib import admin

from moocng.assets.models import Reservation, Asset, AssetAvailability

from moocng.assets.forms import AssetForm, ReservationForm, AssetAvailabilityForm


class AssetAdmin(admin.ModelAdmin):

    form = AssetForm
    #filter_horizontal = ('kq',)


class AssetAvailabilityAdmin(admin.ModelAdmin):

    form = AssetAvailabilityForm
    filter_horizontal = ('assets',)


class ReservationAdmin(admin.ModelAdmin):

    form = ReservationForm
    list_display = ('reserved_from', 'asset', 'user')
    list_filter = ('reserved_from', 'asset', 'user')

admin.site.register(Asset, AssetAdmin)
admin.site.register(AssetAvailability, AssetAvailabilityAdmin)
admin.site.register(Reservation, ReservationAdmin)
