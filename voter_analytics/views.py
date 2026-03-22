# File: views.py
# Author: Letitia Caspersen (letitiac@bu.edu), 3/22/2026
# Description: View classes for the voter_analytics web application

from django.views.generic import ListView, DetailView
from .models import Voter
import plotly
import plotly.graph_objs as go

class VoterListView(ListView):
    """View to display a paginated, filterable list of voter records."""

    template_name = 'voter_analytics/voters.html'
    model = Voter
    context_object_name = 'voters'
    paginate_by = 100

    def get_queryset(self):
        """Return voters filtered by any form fields submitted via GET."""

        qs = super().get_queryset()

        # Filter by party affiliation
        if 'party' in self.request.GET:
            party = self.request.GET['party']
            if party:
                qs = qs.filter(party_affiliation=party)

        # Filter by minimum birth year
        if 'min_dob' in self.request.GET:
            min_dob = self.request.GET['min_dob']
            if min_dob:
                qs = qs.filter(date_of_birth__year__gte=min_dob)

        # Filter by maximum birth year
        if 'max_dob' in self.request.GET:
            max_dob = self.request.GET['max_dob']
            if max_dob:
                qs = qs.filter(date_of_birth__year__lte=max_dob)

        # Filter by voter score
        if 'voter_score' in self.request.GET:
            voter_score = self.request.GET['voter_score']
            if voter_score:
                qs = qs.filter(voter_score=voter_score)

        # Filter by specific election participation checkboxes
        for field in ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']:
            if self.request.GET.get(field):
                qs = qs.filter(**{field: True})

        return qs

    def get_context_data(self, **kwargs):
        """Add filter form options and previously selected values to context."""

        context = super().get_context_data(**kwargs)

        # Populate form dropdown options
        context['parties'] = Voter.objects.values_list('party_affiliation', flat=True).distinct().order_by('party_affiliation')
        context['years'] = range(1900, 2024)
        context['scores'] = range(0, 6)

        # Preserve previously selected form values for pre-selection
        context['selected_party'] = self.request.GET.get('party', '')
        context['selected_min_dob'] = self.request.GET.get('min_dob', '')
        context['selected_max_dob'] = self.request.GET.get('max_dob', '')
        context['selected_voter_score'] = self.request.GET.get('voter_score', '')
        context['selected_v20state'] = self.request.GET.get('v20state', '')
        context['selected_v21town'] = self.request.GET.get('v21town', '')
        context['selected_v21primary'] = self.request.GET.get('v21primary', '')
        context['selected_v22general'] = self.request.GET.get('v22general', '')
        context['selected_v23town'] = self.request.GET.get('v23town', '')

        return context


class GraphsListView(ListView):
    """View to display plotly graphs of aggregate voter data, with filtering."""

    template_name = 'voter_analytics/graphs.html'
    model = Voter
    context_object_name = 'voters'

    def get_queryset(self):
        """Return voters filtered by any form fields submitted via GET."""

        qs = super().get_queryset()

        # Filter by party affiliation
        if 'party' in self.request.GET:
            party = self.request.GET['party']
            if party:
                qs = qs.filter(party_affiliation=party)

        # Filter by minimum birth year
        if 'min_dob' in self.request.GET:
            min_dob = self.request.GET['min_dob']
            if min_dob:
                qs = qs.filter(date_of_birth__year__gte=min_dob)

        # Filter by maximum birth year
        if 'max_dob' in self.request.GET:
            max_dob = self.request.GET['max_dob']
            if max_dob:
                qs = qs.filter(date_of_birth__year__lte=max_dob)

        # Filter by voter score
        if 'voter_score' in self.request.GET:
            voter_score = self.request.GET['voter_score']
            if voter_score:
                qs = qs.filter(voter_score=voter_score)

        # Filter by specific election participation checkboxes
        for field in ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']:
            if self.request.GET.get(field):
                qs = qs.filter(**{field: True})

        return qs

    def get_context_data(self, **kwargs):
        """Add filter form options, previously selected values, and graph divs to context."""

        context = super().get_context_data(**kwargs)

        # Populate form dropdown options
        context['parties'] = Voter.objects.values_list('party_affiliation', flat=True).distinct().order_by('party_affiliation')
        context['years'] = range(1900, 2024)
        context['scores'] = range(0, 6)

        # Preserve previously selected form values for pre-selection
        context['selected_party'] = self.request.GET.get('party', '')
        context['selected_min_dob'] = self.request.GET.get('min_dob', '')
        context['selected_max_dob'] = self.request.GET.get('max_dob', '')
        context['selected_voter_score'] = self.request.GET.get('voter_score', '')
        context['selected_v20state'] = self.request.GET.get('v20state', '')
        context['selected_v21town'] = self.request.GET.get('v21town', '')
        context['selected_v21primary'] = self.request.GET.get('v21primary', '')
        context['selected_v22general'] = self.request.GET.get('v22general', '')
        context['selected_v23town'] = self.request.GET.get('v23town', '')

        qs = self.get_queryset()

        # Graph 1: histogram of voters by birth year
        birth_years = [v.date_of_birth.year for v in qs]
        fig1 = go.Histogram(x=birth_years)
        context['graph_birth_year'] = plotly.offline.plot(
            {"data": [fig1], "layout_title_text": "Voter Distribution by Year of Birth"},
            auto_open=False, output_type="div"
        )

        # Graph 2: pie chart of voters by party affiliation
        party_counts = {}
        for v in qs:
            p = v.party_affiliation.strip()
            party_counts[p] = party_counts.get(p, 0) + 1
        fig2 = go.Pie(labels=list(party_counts.keys()), values=list(party_counts.values()))
        context['graph_party'] = plotly.offline.plot(
            {"data": [fig2], "layout_title_text": "Voter Distribution by Party Affiliation"},
            auto_open=False, output_type="div"
        )

        # Graph 3: bar chart of participation count per election
        elections = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']
        labels = ['2020 State', '2021 Town', '2021 Primary', '2022 General', '2023 Town']
        counts = [qs.filter(**{e: True}).count() for e in elections]
        fig3 = go.Bar(x=labels, y=counts)
        context['graph_elections'] = plotly.offline.plot(
            {"data": [fig3], "layout_title_text": "Vote Count by Election"},
            auto_open=False, output_type="div"
        )

        return context


class VoterDetailView(DetailView):
    """View to display all fields for a single voter record."""

    template_name = 'voter_analytics/voter.html'
    model = Voter
    context_object_name = 'voter'
