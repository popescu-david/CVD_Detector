from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Pacient
from .forms import FormularPacient
import numpy as np
import pandas as pd
import joblib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import base64
import io

@login_required
def home(request):
    qs = Pacient.objects.all()

    filters = {
        'NSS__icontains': request.GET.get('NSS_contains'),
        'Prenume__icontains': request.GET.get('Prenume_contains'),
        'Nume__icontains': request.GET.get('Nume_contains'),
        'Email__icontains': request.GET.get('Email_contains'),
        'Înălțime__gte': request.GET.get('Înălțime_gte'),
        'Înălțime__lte': request.GET.get('Înălțime_lte'),
        'Greutate__gte': request.GET.get('Greutate_gte'),
        'Greutate__lte': request.GET.get('Greutate_lte'),
        'TMS__gte': request.GET.get('TMS_gte'),
        'TMS__lte': request.GET.get('TMS_lte'),
        'TMD__gte': request.GET.get('TMD_gte'),
        'TMD__lte': request.GET.get('TMD_lte'),
        'Colesterol': request.GET.get('Colesterol'),
        'Glucoză': request.GET.get('Glucoză'),
        'Fumător': request.GET.get('Fumător'),
        'Băutor': request.GET.get('Băutor'),
        'Activ': request.GET.get('Activ'),
        'Risc_Boală__gte': request.GET.get('Risc_Boală_gte'),
        'Risc_Boală__lte': request.GET.get('Risc_Boală_lte'),
        'Sex': request.GET.get('Sex'),
        'Vârstă__gte': request.GET.get('Vârstă_gte'),
        'Vârstă__lte': request.GET.get('Vârstă_lte'),
        'Dată_Adăugare_date__gte': request.GET.get('Dată_Adăugare_date_gte'),
        'Dată_Adăugare_date__lte': request.GET.get('Dată_Adăugare_date_lte'),
    }

    for filter_key, filter_value in filters.items():
        if filter_value:
            qs = qs.filter(**{filter_key: filter_value})

    qs = qs.order_by('-Dată_Adăugare')

    paginator = Paginator(qs, 25)
    page = request.GET.get('page')
    try:
        patients = paginator.page(page)
    except PageNotAnInteger:
        patients = paginator.page(1)
    except EmptyPage:
        patients = paginator.page(paginator.num_pages)

    model = joblib.load('Models/Models/XG_Boost/xgb_model.pkl')
    scaler = joblib.load('Models/Models/scaler.pkl')
    model_columns = ['Vârstă', 'Sex', 'Înălțime', 'Greutate', 'TAS', 'TAD', 'Colesterol', 'Glucoză', 'Fumător', 'Băutor', 'Activitate']
    continuous_columns = ['Vârstă', 'Înălțime', 'Greutate', 'TAS', 'TAD']
    
    if request.method == 'POST' and 'action' in request.POST:
        action = request.POST.get('action')
        if action == 'delete':
            patient_id = request.POST.get('patientId')
            patient = get_object_or_404(Pacient, id=patient_id)
            patient.delete()
            return redirect('home')
        elif action == 'add_patient':
            form = FormularPacient(request.POST)
            if form.is_valid():
                new_patient = form.save(commit=False)
                patient_data = {col: getattr(new_patient, col, 0) for col in model_columns}
                patient_df = pd.DataFrame([patient_data])
                continuous_data = patient_df[continuous_columns]
                categorical_data = patient_df.drop(columns=continuous_columns)
                normalized_continuous_data = scaler.transform(continuous_data)
                normalized_patient_data = pd.DataFrame(normalized_continuous_data, columns=continuous_columns).join(categorical_data.reset_index(drop=True))
                model_input = normalized_patient_data.iloc[0].tolist()
                new_patient.Risc_Boală = model.predict([model_input])[0]
                new_patient.save()
                return redirect('home')
    form = FormularPacient()

    return render(request, 'Detector/home.html', {'patients': patients, 'form': form})

@login_required
def patient_detail(request, NSS):
    patient_queryset = Pacient.objects.filter(NSS=NSS).order_by('Dată_Adăugare')
    column_options = ['Vârstă', 'Înălțime', 'Greutate', 'TAS', 'TAD', 'Colesterol', 'Glucoză', 'Fumător', 'Băutor', 'Activitate', 'Risc_Boală']
    selected_columns = column_options
    if request.method == 'POST' and 'action' in request.POST:
        action = request.POST.get('action')
        if action == 'delete':
            patient_id = request.POST.get('patientId')
            patient = get_object_or_404(Pacient, id=patient_id)
            patient.delete()
            if not Pacient.objects.filter(NSS=NSS).exists():
                return redirect('home')
        elif action == 'select_column':
            selected_columns = request.POST.getlist('columns')

    def calculate_percentiles(patient_values, training_data, selected_columns):
        detailed_percentages = []
        bottom_limits = {
            'Vârstă': [0, 17000, 23000],
            'Înălțime': [0, 150, 180],
            'Greutate': [0, 70, 90],
            'TAS': [0, 120, 140],
            'TAD': [0, 80, 90],
            'Risc_Boală': [0, 0.5, 0.8],
        }
        for values in patient_values:
            patient_percentages = {}
            for field in selected_columns:
                patient_value = values[field]
                field_percentages = {}
                if field in ['Fumător', 'Băutor', 'Activitate']:
                    total_count = len(training_data)
                    categories = {'Da': 1, 'Nu': 0}
                    field_percentages = {category: round((training_data[field] == value).sum() / total_count * 100)
                                         for category, value in categories.items()}
                    field_percentages = {k: v for k, v in field_percentages.items()}
                elif field in ['Glucoză', 'Colesterol']:
                    categories = {1: 'Normal', 2: 'Peste Limita Normală', 3: 'Mult Peste Limita Normală'}
                    field_percentages = {desc: round((training_data[field] == value).sum() / len(training_data) * 100)
                                         for value, desc in categories.items()}
                    patient_category = categories[patient_value]
                    field_percentages = {k: v for k, v in field_percentages.items() if list(categories.values()).index(k) <= list(categories.values()).index(patient_category)}
                else:
                    total_count = len(training_data)
                    limits = bottom_limits.get(field, [0])
                    categories = ['Normal', 'Peste Limita Normală', 'Mult Peste Limita Normală']
                    cumulative_percentage = 0
                    cumulative_field_percentages = []
                    for i in range(len(limits) - 1):
                        category_percentage = round(((training_data[field] > limits[i]) & (training_data[field] <= limits[i+1])).sum() / total_count * 100)
                        cumulative_percentage += category_percentage
                        cumulative_field_percentages.append(cumulative_percentage)
                    cumulative_field_percentages.append(cumulative_percentage + round((training_data[field] > limits[-1]).sum() / total_count * 100))
                    below_percentage = round((training_data[field] < patient_value).sum() / total_count * 100)
                    previous_sum = 0
                    for i, category in enumerate(categories):
                        top_end = cumulative_field_percentages[i]
                        field_percentages[category] = min(below_percentage, top_end) - previous_sum
                        previous_sum += field_percentages[category]
                    if field_percentages['Normal'] < 5 and field_percentages['Peste Limita Normală'] == 0 and field_percentages['Mult Peste Limita Normală'] == 0:
                        field_percentages['Normal'] = 5
                patient_percentages[field] = (patient_value, field_percentages)
            detailed_percentages.append(patient_percentages)
        return detailed_percentages

    def generate_column_chart(patient_data, percentages, selected_columns):
        dates = [pd.to_datetime(data.Dată_Adăugare) for data in patient_data]
        unique_dates = sorted(set(dates))
        fig, ax = plt.subplots(figsize=(14, 7))
        bar_width = 0.8 / len(selected_columns)
        columns = {
            "Vârstă": {"color": "#2E8B57", "opacity": {"Normal": 0.4, "Peste Limita Normală": 0.7, "Mult Peste Limita Normală": 1.0}},
            "Înălțime": {"color": "#556B2F", "opacity": {"Normal": 0.4, "Peste Limita Normală": 0.7, "Mult Peste Limita Normală": 1.0}},
            "Greutate": {"color": "#FF8C00", "opacity": {"Normal": 0.4, "Peste Limita Normală": 0.7, "Mult Peste Limita Normală": 1.0}},
            "TAS": {"color": "#8B0000", "opacity": {"Normal": 0.4, "Peste Limita Normală": 0.7, "Mult Peste Limita Normală": 1.0}},
            "TAD": {"color": "#DAA520", "opacity": {"Normal": 0.4, "Peste Limita Normală": 0.7, "Mult Peste Limita Normală": 1.0}},
            "Colesterol": {"color": "#A0522D", "opacity": {"Normal": 0.4, "Peste Limita Normală": 0.7, "Mult Peste Limita Normală": 1.0}},
            "Glucoză": {"color": "#708090", "opacity": {"Normal": 0.4, "Peste Limita Normală": 0.7, "Mult Peste Limita Normală": 1.0}},
            "Risc_Boală": {"color": "#708123", "opacity": {"Normal": 0.4, "Peste Limita Normală": 0.7, "Mult Peste Limita Normală": 1.0}},
            "Fumător": {"color": "#2E8B57", "opacity": {"Nu": 0.4, "Da": 0.7}},
            "Băutor": {"color": "#FF8C00", "opacity": {"Nu": 0.4, "Da": 0.7}},
            "Activitate": {"color": "#DAA520", "opacity": {"Nu": 0.7, "Da": 0.4}},
        }
        for i, field in enumerate(selected_columns):
            if field not in columns:
                continue
            category_opacities = columns[field]["opacity"]
            field_values = {category: [0] * len(unique_dates) for category in category_opacities.keys()}
            for j in range(len(patient_data)):
                patient_values, field_percentages = percentages[j].get(field, (0, {}))
                for cat, percent in field_percentages.items():
                    if cat in field_values:
                        field_values[cat][dates.index(patient_data[j].Dată_Adăugare)] += percent
            base_color = columns[field]["color"]
            ordered_categories = {
                "Vârstă": ["Normal", "Peste Limita Normală", "Mult Peste Limita Normală"],
                "Înălțime": ["Normal", "Peste Limita Normală", "Mult Peste Limita Normală"],
                "Greutate": ["Normal", "Peste Limita Normală", "Mult Peste Limita Normală"],
                "TAS": ["Normal", "Peste Limita Normală", "Mult Peste Limita Normală"],
                "TAD": ["Normal", "Peste Limita Normală", "Mult Peste Limita Normală"],
                "Colesterol": ["Normal", "Peste Limita Normală", "Mult Peste Limita Normală"],
                "Glucoză": ["Normal", "Peste Limita Normală", "Mult Peste Limita Normală"],
                "Risc_Boală": ["Normal", "Peste Limita Normală", "Mult Peste Limita Normală"],
                "Fumător": ["Nu", "Da"],
                "Băutor": ["Nu", "Da"],
                "Activitate": ["Da", "Nu"],
            }
            cumulative_values = [0] * len(unique_dates)
            for category in ordered_categories[field]:
                if category in field_values:
                    values = field_values[category]
                    opacity = category_opacities[category]
                    color = plt.cm.colors.to_rgba(base_color, alpha=opacity)
                    ax.bar(
                        np.arange(len(unique_dates)) + i * bar_width,
                        values,
                        bar_width,
                        bottom=cumulative_values,
                        label=f'{field} {category}',
                        color=color
                    )
                    cumulative_values = [sum(x) for x in zip(cumulative_values, values)]

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight')
        buffer.seek(0)
        plt.close(fig)
        graph_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        return graph_base64

    model = joblib.load('Models/Models/XG_Boost/xgb_model.pkl')
    scaler = joblib.load('Models/Models/scaler.pkl')
    baseline = pd.read_csv('Models/Datasets/xgb_enhanced_cardio_train.csv')
    
    def generate_risk_reasons(patient):
        model_features = model.feature_names_in_
        feature_importances = model.feature_importances_
        continuous_columns = ['Vârstă', 'Înălțime', 'Greutate', 'TAS', 'TAD']
        categorical_columns = ['Sex', 'Colesterol', 'Glucoză', 'Fumător', 'Băutor', 'Activitate']
        patient_data = {
            'Vârstă': patient.Vârstă,
            'Sex': patient.Sex,
            'Înălțime': patient.Înălțime,
            'Greutate': patient.Greutate,
            'TAS': patient.TAS,
            'TAD': patient.TAD,
            'Colesterol': patient.Colesterol,
            'Glucoză': patient.Glucoză,
            'Fumător': patient.Fumător,
            'Băutor': patient.Băutor,
            'Activitate': patient.Activitate
        }
        patient_df = pd.DataFrame([patient_data])
        continuous_data = patient_df[continuous_columns]
        categorical_data = patient_df[categorical_columns]
        normalized_continuous_data = scaler.transform(continuous_data)
        normalized_patient_data = pd.DataFrame(normalized_continuous_data, columns=continuous_columns).join(categorical_data.reset_index(drop=True))
        normalized_patient_data = normalized_patient_data[model_features]
        model_input = normalized_patient_data.iloc[0].tolist()
        reasons = {col: feature_importances[i] * model_input[i] for i, col in enumerate(model_features)}
        sorted_reasons = sorted(reasons.items(), key=lambda item: item[1], reverse=True)
        return sorted_reasons

    patient_values = list(patient_queryset.values(*selected_columns))
    detailed_percentages = calculate_percentiles(patient_values, baseline, selected_columns)
    column_chart_base64 = generate_column_chart(patient_queryset, detailed_percentages, selected_columns)
    patient_details = []
    for patient in patient_queryset:
        entry = {
            'date': patient.Dată_Adăugare,
            'risk': patient.Risc_Boală,
            'reasons': generate_risk_reasons(patient)
        }
        patient_details.append(entry)
    max_reasons = max(len(detail['reasons']) for detail in patient_details)
    
    return render(request, 'Detector/patient_detail.html', {
        'patients': patient_queryset,
        'selected_columns': selected_columns,
        'column_options': column_options,
        'column_chart_base64': column_chart_base64,
        'patient_details': patient_details,
        'max_reasons': range(max_reasons)
    })

def about(request):
    return render(request, 'Detector/about.html')

