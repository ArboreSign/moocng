# Copyright 2012 Rooter Analysis S.L.
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
import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.conf import settings

from moocng.badges.models import Badge, Award, BadgeAssertion
from moocng.badges.utils import get_openbadge_public_key


def user_badges(request, user_pk, mode):
    if mode == 'email':
        user = get_object_or_404(User, email=user_pk)
    else:
        user = get_object_or_404(User, id=user_pk)
    try:
        award_list = Award.objects.filter(user=user)
        return render_to_response('badges/user_badges.html', {
            'award_list': award_list,
            'user': user,
            'openbadges_base_url': settings.OPENBADGES_BASE_URL,
        }, context_instance=RequestContext(request))
    except Award.DoesNotExist:
        return HttpResponse(status=404)


def user_badge(request, badge_slug, user_pk, mode):
    badge = get_object_or_404(Badge, slug=badge_slug)
    if mode == 'email':
        user = get_object_or_404(User, email=user_pk)
    else:
        user = get_object_or_404(User, id=user_pk)
    try:
        award = get_object_or_404(Award, badge=badge, user=user)
        return render_to_response('badges/user_badge.html', {
            'award': award,
            'user': user,
            'openbadges_base_url': settings.OPENBADGES_BASE_URL,
        }, context_instance=RequestContext(request))
    except Award.DoesNotExist:
        return HttpResponse(status=404)


def badge_image(request, badge_slug, user_pk, mode):
    badge = get_object_or_404(Badge, slug=badge_slug)
    if mode == 'email':
        user = get_object_or_404(User, email=user_pk)
    else:
        user = get_object_or_404(User, id=user_pk)
    try:
        Award.objects.filter(user=user).get(badge=badge)
        return HttpResponse(badge.image.read(), content_type="image/png")
    except Award.DoesNotExist:
        return HttpResponse(status=404)

@login_required
def openbadge_assertion(request, badge_slug):
    user = get_object_or_404(User, pk=request.user.pk)
    badge = get_object_or_404(Badge, slug=badge_slug)
    badge_assertion = BadgeAssertion.objects.get(user=user, award__badge=badge)
    badge_assertion_json = badge_assertion.as_json_web_signature()
    return HttpResponse(badge_assertion_json, mimetype='application/json')


def openbadge_issuer(request):
    current_site = Site.objects.get_current()
    issuer_json = {
        'name': current_site.name,
        'url': 'http://%s' % current_site.domain
    }
    return HttpResponse(json.dumps(issuer_json), mimetype='application/json')


def openbadge_public_key(request):
    public_key = get_openbadge_public_key()
    # TODO content_type is correct?
    return HttpResponse(public_key, content_type='text/plain')
