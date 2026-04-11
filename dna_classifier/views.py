"""
DNA Classifier views - Home, Dashboard, Input, Result, History, Admin, Export.
"""
import json
import logging
from datetime import datetime, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.db.models import Count
from django.utils import timezone
from django.core.paginator import Paginator

from .models import DNASequence, APILog
from .utils import clean_sequence, validate_sequence, get_sequence_stats, colorize_sequence_html
from .predictor import get_predictor
from .ai_helper import get_ai_explanation, get_ai_suggestions

logger = logging.getLogger(__name__)


@login_required
def model_accuracy_view(request):
    """Run model accuracy check and display report."""
    predictor = get_predictor()
    
    # Test sequences with known labels (same as in verify_accuracy.py)
    test_data = [
        ("ATGTTTTGCCAACTGGCCAAGACCTGCCCTGTGCAGCTGTGGGTTGATTCCACACCCCCGCCCGGCACCCGCGTCCGCGCCATGGCCATCTACAAGCAGTCACAGCACATGACGGAGGTTGTGAGGCGCTGCCCCCACCATGAGCGCTGCTCAGATAGCGATGGTCTGGCCCCTCCTCAGCATCTTATCCGAGTGGAAGGAAATTTGCGTGTGGAGTATTTGGATGACAGAAACACTTTTCGACATAGTGTGGTGGTGCCCTATGAGCCGCCTGAGGTTGGCTCTGACTGTACCACCATCCACTACAACTACATGTGTAACAGTTCCTGCATGGGCGGCATGAACCGGAGGCCCATCCTCACCATCATCACACTGGAAGACTCCAGTGGTAATCTACTGGGACGGAACAGCTTTGAGGTGCGTGTTTGTGCCTGTCCTGGGAGAGACCGGCGCACAGAGGAAGAGAATCTCCGCAAGAAAGGGGAGCCTCACCACGAGCTGCCCCCAGGGAGCACTAAGCGAGCACTGCCCAACAACACCAGCTCCTCTCCCCAGCCAAAGAAGAAACCACTGGATGGAGAATATTTCACCCTTCAGATCCGTGGGCGTGAGCGCTTCGAGATGTTCCGAGAGCTGAATGAGGCCTTGGAACTCAAGCCGTACTCCCCGGACGAT", "human"),
        ("ATGCAGCAGCCCCGGCAGCAGCAGCAGCAGCAAAGCAAGATCAGCAGCAACAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAG", "chimpanzee"),
        ("ATGGGAATCCCAGAAGGAAAGTCAGCTTGCAAATGGAATGGATTTCCAGCAGTAGCAGCCCAGCCCCCGGAGCCACAGCCCCCAGCCCCAGCCCCAGCACCCAGCACCCGGCCGCAGCACCCGGAGAGCAGCAGAGCCCAGCAAGGCAGCAGCAGCAGCAGCAGATCAAGAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAG", "dog"),
    ]
    
    results = []
    correct = 0
    total = len(test_data)
    
    for seq, expected in test_data:
        try:
            # Clean and validate (simple version)
            prepared_seq = seq.upper().replace(' ', '').replace('\n', '')
            result = predictor.predict(prepared_seq)
            predicted = result['label']
            confidence = result['confidence']
            
            is_correct = predicted.lower() == expected.lower()
            if is_correct:
                correct += 1
            
            results.append({
                'expected': expected,
                'predicted': predicted,
                'confidence': confidence,
                'is_correct': is_correct,
                'status': "PASS" if is_correct else "FAIL"
            })
        except Exception as e:
            logger.error(f"Error checking accuracy for {expected}: {e}")
            results.append({
                'expected': expected,
                'predicted': "ERROR",
                'confidence': 0,
                'is_correct': False,
                'status': f"ERROR: {str(e)}"
            })

    accuracy = (correct / total) * 100 if total > 0 else 0
    
    context = {
        'results': results,
        'total': total,
        'correct': correct,
        'accuracy': round(accuracy, 1),
        'title': 'Model Accuracy Report',
        'report_date': timezone.now()
    }
    return render(request, 'accuracy_report.html', context)


def home_view(request):
    """Landing page with project overview."""
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('admin_dashboard')
        return redirect('dashboard')
    stats = {
        'total_predictions': DNASequence.objects.count(),
        'total_users': User.objects.count(),
        'today_predictions': DNASequence.objects.filter(
            created_at__date=timezone.now().date()
        ).count(),
    }
    return render(request, 'home.html', {'stats': stats, 'title': 'DNA Classification System'})


@login_required
def dashboard_view(request):
    """User dashboard with stats and recent predictions."""
    if request.user.is_staff:
        return redirect('admin_dashboard')
        
    user_predictions = DNASequence.objects.filter(user=request.user)

    # Stats
    total = user_predictions.count()
    today_count = user_predictions.filter(created_at__date=timezone.now().date()).count()
    recent_5 = user_predictions[:5]

    # Class distribution for Chart.js
    class_dist = (
        user_predictions.values('prediction')
        .annotate(count=Count('id'))
        .order_by('-count')
    )
    chart_labels = [item['prediction'] for item in class_dist]
    chart_values = [item['count'] for item in class_dist]

    # Last 7 days activity
    last_7 = []
    for i in range(6, -1, -1):
        day = timezone.now().date() - timedelta(days=i)
        count = user_predictions.filter(created_at__date=day).count()
        last_7.append({'date': day.strftime('%b %d'), 'count': count})

    context = {
        'total_predictions': total,
        'today_predictions': today_count,
        'recent_predictions': recent_5,
        'chart_labels': json.dumps(chart_labels),
        'chart_values': json.dumps(chart_values),
        'last_7_days': json.dumps(last_7),
        'title': 'Dashboard',
    }
    return render(request, 'dashboard.html', context)


@login_required
def dna_input_view(request):
    """DNA sequence input page - handles validation and prediction."""
    if request.method == 'POST':
        raw_sequence = request.POST.get('sequence', '')
        cleaned = clean_sequence(raw_sequence)
        is_valid, error_msg = validate_sequence(cleaned)

        if not is_valid:
            messages.error(request, f"❌ {error_msg}")
            return render(request, 'dna_input.html', {
                'sequence': raw_sequence,
                'title': 'Classify DNA Sequence'
            })

        try:
            # Run ML prediction
            predictor = get_predictor()
            result = predictor.predict(cleaned)

            # AI generation disabled as requested
            ai_explanation = ""
            ai_suggestions = ""

            # Save to database
            dna_record = DNASequence.objects.create(
                user=request.user,
                sequence=cleaned,
                prediction=result['label'],
                confidence_score=result['confidence'],
                ai_explanation=ai_explanation,
                ai_suggestions=ai_suggestions,
            )
            # Store probabilities in session so result page can access them
            request.session[f'probs_{dna_record.pk}'] = result.get('probabilities', {})
            return redirect('result', pk=dna_record.pk)

        except RuntimeError as e:
            messages.error(request, f"Model error: {e}")
        except Exception as e:
            logger.error(f"Classification error: {e}")
            messages.error(request, "Classification failed. Please try again.")

    return render(request, 'dna_input.html', {'title': 'Classify DNA Sequence'})


@login_required
def result_view(request, pk):
    """Display classification result with AI explanation and class probabilities."""
    record = get_object_or_404(DNASequence, pk=pk, user=request.user)
    stats = get_sequence_stats(record.sequence)
    colored_html = colorize_sequence_html(record.sequence[:300])

    # Retrieve stored probabilities from session (set during classification)
    probs = request.session.pop(f'probs_{pk}', {})

    # Convert probs for Chart.js
    prob_labels = json.dumps(list(probs.keys()))
    prob_values = json.dumps([round(v * 100, 1) for v in probs.values()])

    context = {
        'record': record,
        'stats': stats,
        'colored_sequence': colored_html,
        'prob_labels': prob_labels,
        'prob_values': prob_values,
        'title': f'Result - {record.prediction}',
    }
    return render(request, 'result.html', context)



@login_required
def history_view(request):
    """Paginated history of user's DNA predictions with search."""
    query = request.GET.get('q', '')
    predictions = DNASequence.objects.filter(user=request.user)

    if query:
        predictions = predictions.filter(prediction__icontains=query) | \
                      predictions.filter(sequence__icontains=query)

    paginator = Paginator(predictions.order_by('-created_at'), 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'query': query,
        'total_count': predictions.count(),
        'title': 'Prediction History',
    }
    return render(request, 'history.html', context)


@login_required
def history_detail_view(request, pk):
    """Single prediction detail view."""
    record = get_object_or_404(DNASequence, pk=pk, user=request.user)
    stats = get_sequence_stats(record.sequence)
    colored_html = colorize_sequence_html(record.sequence[:300])

    return render(request, 'result.html', {
        'record': record,
        'stats': stats,
        'colored_sequence': colored_html,
        'title': f'Detail - {record.prediction}',
    })


@login_required
def export_pdf_view(request, pk):
    """Export a DNA prediction result as a PDF."""
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib import colors
    from reportlab.lib.units import inch
    import io

    record = get_object_or_404(DNASequence, pk=pk, user=request.user)
    stats = get_sequence_stats(record.sequence)

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch)
    styles = getSampleStyleSheet()
    story = []

    # Title
    title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'],
                                  fontSize=20, textColor=colors.HexColor('#1e40af'))
    story.append(Paragraph("🧬 DNA Classification Report", title_style))
    story.append(Spacer(1, 0.2*inch))

    # Metadata table
    meta_data = [
        ['Report Date', record.created_at.strftime('%Y-%m-%d %H:%M UTC')],
        ['User', request.user.username],
        ['Predicted Class', record.prediction],
        ['Confidence', record.confidence_percent],
        ['Sequence Length', f"{stats.get('length', 0)} bp"],
        ['GC Content', f"{stats.get('gc_content', 0)}%"],
    ]
    meta_table = Table(meta_data, colWidths=[2*inch, 4*inch])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#dbeafe')),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.HexColor('#f0f9ff')]),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 0.2*inch))

    # Sequence
    story.append(Paragraph("DNA Sequence", styles['Heading2']))
    seq_display = record.sequence[:500] + ('...' if len(record.sequence) > 500 else '')
    story.append(Paragraph(f'<font name="Courier" size="8">{seq_display}</font>', styles['Normal']))
    story.append(Spacer(1, 0.2*inch))


    doc.build(story)
    buffer.seek(0)

    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="dna_report_{pk}.pdf"'
    return response


@login_required
def analytics_api_view(request):
    """REST endpoint returning analytics data for Chart.js."""
    user_predictions = DNASequence.objects.filter(user=request.user)

    class_dist = list(
        user_predictions.values('prediction').annotate(count=Count('id')).order_by('-count')
    )

    last_7 = []
    for i in range(6, -1, -1):
        day = timezone.now().date() - timedelta(days=i)
        count = user_predictions.filter(created_at__date=day).count()
        last_7.append({'date': day.strftime('%b %d'), 'count': count})

    return JsonResponse({
        'class_distribution': class_dist,
        'last_7_days': last_7,
        'total': user_predictions.count(),
    })


def is_admin(user):
    return user.is_authenticated and user.is_staff


@user_passes_test(is_admin, login_url='/users/login/')
def admin_dashboard_view(request):
    """Custom admin analytics dashboard."""
    total_users = User.objects.count()
    total_predictions = DNASequence.objects.count()
    today_predictions = DNASequence.objects.filter(
        created_at__date=timezone.now().date()
    ).count()
    
    # We remove api_logs as requested by user
    # api_logs = APILog.objects.all()[:20]

    class_dist = list(
        DNASequence.objects.values('prediction').annotate(count=Count('id')).order_by('-count')
    )

    # Active users (made a prediction in last 7 days)
    week_ago = timezone.now() - timedelta(days=7)
    active_users = DNASequence.objects.filter(
        created_at__gte=week_ago
    ).values('user').distinct().count()

    # Increase limit for the new Global History section
    recent_predictions = DNASequence.objects.select_related('user').order_by('-created_at')[:20]

    # All users with prediction counts and profiles (select_related for team_name)
    all_users = User.objects.select_related('profile').annotate(
        prediction_count=Count('dnasequence_set')
    ).order_by('-date_joined')
    
    for u in all_users:
        if total_predictions > 0:
            u.prediction_percent = min(100, (u.prediction_count / total_predictions) * 100)
        else:
            u.prediction_percent = 0

    context = {
        'total_users': total_users,
        'total_predictions': total_predictions,
        'today_predictions': today_predictions,
        'active_users': active_users,
        'class_dist': json.dumps(class_dist),
        'recent_predictions': recent_predictions,
        'all_users': all_users,
        'title': 'Admin Analytics Dashboard',
    }
    return render(request, 'admin_dashboard.html', context)
