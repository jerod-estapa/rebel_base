from django.shortcuts import render_to_response, RequestContext
from django.views.generic import TemplateView
from payments.models import User
from .models import MarketingItem, StatusReport, Announcement
from datetime import date, timedelta
# from main.templatetags.main_marketing import marketing__circle_item


class market_item(object):

    def __init__(self, img, heading, caption, button_link="register", button_title="View details"):
        self.img = img
        self.heading = heading
        self.caption = caption
        self.button_link = button_link
        self.button_title = button_title

market_items = [
    market_item(
        img="yoda.jpg",
        heading="Hone Your Jedi Skills",
        caption="All members have access to our unique"
        " training and achievements ladders. Progress through the "
        "levels and show everyone who the top Jedi Master is!",
        button_title="Sign Up Now"
    ),

    market_item(
        img="clone_army.jpg",
        heading="Build Your Clan",
        caption="Engage in meaningful conversation, or "
                "bloodthirsty battle! If it's Star Wars, it's here!",
        button_title="Sign Up Now"
    ),

    market_item(
        img="leia.jpg",
        heading="Find Love",
        caption="Everyone knows Star Wars fans are the "
                "best mates for Star Wars fans. Find your "
                "Princess Leia or Han Solo and explore the "
                "stars together.",
        button_title="Sign Up Now"
    ),
]


def index(request):
    uid = request.session.get('user')
    if uid is None:
        # main landing page
        market_items = MarketingItem.objects.all()
        return render_to_response(
            'main/index.html',
            {'marketing_items': market_items}
        )
    else:
        # membership page
        status = StatusReport.objects.all().order_by('-when')[:20]
        announce_date = date.today() - timedelta(days=30)
        announce = (Announcement.objects.filter(
         when__gt=announce_date).order_by('-when')
                    )
        return render_to_response(
            'main/user.html',
            {
                'user': User.get_by_id(uid),
                'reports': status,
                'announce': announce
            },
            context_instance=RequestContext(request),
        )


class AboutPageView(TemplateView):
    template_name = 'main/about.html'


def report(request):
    if request.method == "POST":
        status = request.POST.get("status", "")
        # Update database with the status
        if status:
            uid = request.session.get('user')
            user = User.get_by_id(uid)
            StatusReport(user=user, status=status).save()

        return index(request)
