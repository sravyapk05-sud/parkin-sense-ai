from datetime import datetime
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from myapp.classify import check
from myapp.models import *


#   admin details
#   username : admin@gmail.com
#   password : Admin123
from myapp.report_generator import create_detailed_medical_report
from myapp.voice_pred import predict_audio


def adminhome(request):
    return render(request,'admin/homeindex.html')

def logout(request):
    request.session['lid']=""
    return redirect('/myapp/login/')

# def admin_header(request):
#     return render(request,"admin/admin_headers.html")
#
#
#
def login_get(request):
    return render(request,"login_index.html")
#
#
#
def login_post(request):
    user_name = request.POST['textfield']
    password=request.POST['textfield2']
    user=authenticate(request,username=user_name,password=password)
    if user is not None:
        login(request,user)
        if user.is_superuser:
            return redirect('/myapp/adminhome/')
        elif user.groups.filter(name="expert").exists():
            if Expert.objects.filter(AUTHUSER_id=request.user.id,status="approved").exists():
                return redirect('/myapp/doctornhome/')
            else:
                messages.warning(request, "Admin Didnt Approved Your Request")
                return redirect('/myapp/login_get/')
        else:
            messages.warning(request,"Invalid User")
            return redirect('/myapp/login_get/')
    else:
        messages.warning(request, "Invalid Username or Password")
        return redirect('/myapp/login_get/')


def change_password(request):
    return render(request,'admin/change password.html')

def change_password_post(request):
    current_password=request.POST['textfield']
    new_password=request.POST['textfield2']
    confirm_password=request.POST['textfield3']
    user=request.user
    if not user.check_password(current_password):
        return HttpResponse("<script>alert('Invalid message'); window.location='/myapp/change_password';</script>")
    if new_password == confirm_password:
        user.set_password(confirm_password)
        user.save()
        return HttpResponse("<script>alert('Password changed'); window.location='/myapp/login_get';</script>")
    else:
        return HttpResponse("<script>alert('Password mismatch'); window.location='/myapp/change_password';</script>")




def view_complaint_send_reply(request):
    res=Complaint.objects.all()
    res_pend=Complaint.objects.filter(reply="pending")
    res_rep=Complaint.objects.filter(~Q(reply="pending"))
    return render(request,'admin/view complaint&send reply.html',{'data':res, 'ln_pend':len(res_pend), "ln_rep":len(res_rep)})

def view_comlaint_send_reply_post(request):
    from_date=request.POST['textfield1']
    TO_date=request.POST['textfield2']
    res=Complaint.objects.filter(Date__range=[from_date,TO_date])
    return render(request,'admin/view complaint&send reply.html',{'data':res})



def send_reply(request,id):
    return render(request,'admin/send_reply.html',{'id':id})


def post_send_reply(request):
    cid=request.POST['cid']
    reply=request.POST['reply']
    var=Complaint.objects.get(id=cid)
    var.reply=reply
    var.status='replayed'
    var.save()
    messages.success(request,"Replied Successfull")
    return redirect('/myapp/view_complaint_send/')
    # return HttpResponse('''<script>alert('reply send');window.location='/myapp/view_complaint_send/'</script>''')




def view_doctor(request):
    res=Expert.objects.filter(status='pending')
    res_app=Expert.objects.filter(status='approved')
    res_rej=Expert.objects.filter(status='rejected')
    return render(request,'admin/view doctor.html',{'data':res, 'ln_pend':len(res), "ln_app":len(res_app), "ln_rej":len(res_rej)})


def aprove_doctor(request,id):
    res=Expert.objects.filter(id=id).update(status='approved')
    return HttpResponse('''<script>alert('approved');window.location='/myapp/view_doctor/'</script>''')

def reject_doctors(request,id):
    res=Expert.objects.filter(id=id).update(status='rejected')
    return HttpResponse('''<script>alert('rejected');window.location='/myapp/view_doctor/'</script>''')

def view_approved_doctor(request):
    res=Expert.objects.filter(status='approved')
    return render(request,'admin/view approved doctor.html',{'data':res})

def view_rejected_doctor(request):
    res = Expert.objects.filter(status='rejected')
    return render(request,'admin/view rejected doctor.html',{'data': res})

def view_users(request):
    res = Patient.objects.all()
    print(len(res))
    return render(request,'admin/View users.html',{'data': res,"ln":len(res)})

def view_review_about_doctors(request):
    res=Review.objects.all()
    return render(request,'admin/view review about doctors.html',{"data":res})

def view_review_about_post(request):
    from_date = request.POST['textfield1']
    TO_date = request.POST['textfield2']
    res=Review.objects.filter(Date__range=[from_date,TO_date])
    return render(request,'admin/view review about doctors.html',{"data":res})


def evaluate_model_comprehensive(model_path, test_images, test_labels, class_names):
    """
    Complete evaluation pipeline
    """
    print("=" * 60)
    print("MODEL EVALUATION REPORT")
    print("=" * 60)

    # 1. Load model
    print("\n1. Loading model...")
    graph = load_frozen_model(model_path)
    input_tensor, output_tensor = get_model_io_tensors(graph)

    if input_tensor is None or output_tensor is None:
        print("ERROR: Could not find input/output tensors.")
        print("\nAvailable tensors in your model:")
        ops = graph.get_operations()
        for i, op in enumerate(ops[:20]):  # Show first 20 ops
            print(f"  {op.name}")
        if len(ops) > 20:
            print(f"  ... and {len(ops) - 20} more")
        return None

    # 2. Run predictions
    print("\n2. Running predictions...")
    predictions = predict_batch(graph, input_tensor, output_tensor, test_images)

    # 3. Calculate metrics
    print("\n3. Calculating metrics...")

    # Basic metrics
    accuracy = accuracy_score(test_labels, predictions)

    # For multi-class, use 'macro' average (treats all classes equally)
    precision = precision_score(test_labels, predictions, average='macro', zero_division=0)
    recall = recall_score(test_labels, predictions, average='macro', zero_division=0)
    f1 = f1_score(test_labels, predictions, average='macro', zero_division=0)

    # Weighted averages (considers class imbalance)
    precision_weighted = precision_score(test_labels, predictions, average='weighted', zero_division=0)
    recall_weighted = recall_score(test_labels, predictions, average='weighted', zero_division=0)
    f1_weighted = f1_score(test_labels, predictions, average='weighted', zero_division=0)

    # 4. Display results
    print("\n" + "=" * 60)
    print("EVALUATION METRICS")
    print("=" * 60)

    print(f"\nOverall Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")

    print("\n--- Macro Averages (equal weight per class) ---")
    print(f"Precision: {precision:.4f}")
    print(f"Recall:    {recall:.4f}")
    print(f"F1 Score:  {f1:.4f}")

    print("\n--- Weighted Averages (weighted by class size) ---")
    print(f"Precision: {precision_weighted:.4f}")
    print(f"Recall:    {recall_weighted:.4f}")
    print(f"F1 Score:  {f1_weighted:.4f}")

    # 5. Detailed classification report
    print("\n" + "=" * 60)
    print("DETAILED CLASS-WISE METRICS")
    print("=" * 60)

    report = classification_report(test_labels, predictions,
                                   target_names=class_names,
                                   zero_division=0)
    print(report)

    # 6. Confusion Matrix
    print("\n" + "=" * 60)
    print("CONFUSION MATRIX")
    print("=" * 60)

    cm = confusion_matrix(test_labels, predictions)

    # Display confusion matrix as text (for quick view)
    print("\nConfusion Matrix (rows: true, columns: predicted):")
    print(f"{'':<15}", end="")
    for i in range(min(10, len(class_names))):
        print(f"{i:<4}", end="")
    print("...")

    for i in range(min(10, len(class_names))):
        print(f"{class_names[i][:12]:<12} |", end="")
        for j in range(min(10, len(class_names))):
            print(f"{cm[i,j]:<4}", end="")
        if len(class_names) > 10:
            print("...", end="")
        print()

    # 7. Return all results for further analysis
    results = {
        'accuracy': accuracy,
        'precision_macro': precision,
        'recall_macro': recall,
        'f1_macro': f1,
        'precision_weighted': precision_weighted,
        'recall_weighted': recall_weighted,
        'f1_weighted': f1_weighted,
        'predictions': predictions,
        'confusion_matrix': cm,
        'class_names': class_names
    }

    return results

import tensorflow as tf
import numpy as np
import os
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
from PIL import Image
import warnings
warnings.filterwarnings('ignore')

# Set random seeds for reproducibility
np.random.seed(42)
try:
    # Try TensorFlow 2.x method
    tf.random.set_seed(42)
except AttributeError:
    # Use TensorFlow 1.x method
    tf.set_random_seed(42)


def load_test_dataset_from_folders(test_root_dir, img_size=(224, 224)):
    """
    Load test images from folder structure: test_root_dir/class_name/*.jpg

    Args:
        test_root_dir: Root directory with class subfolders
        img_size: Target image size (height, width)

    Returns:
        images: NumPy array of images
        labels: List of integer labels
        class_names: List of class names (folder names)
        image_paths: List of image file paths
    """
    images = []
    labels = []
    image_paths = []
    class_names = sorted(os.listdir(test_root_dir))

    # Map class names to integer indices
    class_to_idx = {class_name: idx for idx, class_name in enumerate(class_names)}

    print(f"Found {len(class_names)} classes: {class_names}")

    for class_name in class_names:
        class_dir = os.path.join(test_root_dir, class_name)
        if not os.path.isdir(class_dir):
            continue

        class_idx = class_to_idx[class_name]
        image_files = [f for f in os.listdir(class_dir)
                       if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp'))]

        print(f"  {class_name}: {len(image_files)} images")

        for img_file in image_files:
            img_path = os.path.join(class_dir, img_file)

            try:
                # Load and preprocess image
                img = Image.open(img_path).convert('RGB')
                img = img.resize(img_size)
                img_array = np.array(img)

                # Normalize to [0, 1] (adjust if your model expects different normalization)
                img_array = img_array.astype(np.float32) / 255.0

                images.append(img_array)
                labels.append(class_idx)
                image_paths.append(img_path)

            except Exception as e:
                print(f"Error loading {img_path}: {e}")

    print(f"\nTotal loaded: {len(images)} images")
    return np.array(images), np.array(labels), class_names, image_paths


# Usage
test_root_dir = r"C:\Users\isasu\Music\project\web\D_daignosis\myapp\static\mri validation\\"  # Change this to your actual path
test_images, test_labels, class_names, image_paths = load_test_dataset_from_folders(test_root_dir)


def load_frozen_model(pb_file_path):
    """
    Load a frozen TensorFlow model (.pb file)
    """
    # Load the frozen graph
    with tf.io.gfile.GFile(pb_file_path, 'rb') as f:
        graph_def = tf.compat.v1.GraphDef()
        graph_def.ParseFromString(f.read())

    # Import the graph_def into a new Graph
    with tf.Graph().as_default() as graph:
        tf.import_graph_def(graph_def, name='')

    return graph


def get_model_io_tensors(graph):
    """
    Find input and output tensors in the loaded graph
    You might need to adjust these tensor names
    """
    # Common tensor names in TensorFlow models
    possible_input_names = [
        'input:0', 'Placeholder:0', 'input_tensor:0', 'DecodeJpeg:0',
        'inputs:0', 'x:0', 'image_tensor:0'
    ]

    possible_output_names = [
        'output:0', 'final_result:0', 'predictions:0', 'final_training_ops:0',
        'softmax_tensor:0', 'InceptionV3/Predictions/Reshape_1:0',
        'MobilenetV1/Predictions/Reshape_1:0'
    ]

    # List all operations to find the right ones
    ops = graph.get_operations()

    # Find input tensor (usually a placeholder)
    input_tensor = None
    for name in possible_input_names:
        try:
            input_tensor = graph.get_tensor_by_name(name)
            print(f"Found input tensor: {name}")
            break
        except:
            continue

    if input_tensor is None:
        # Try to find by shape (usually has None for batch dimension)
        for op in ops:
            if 'input' in op.name.lower() and len(op.outputs) == 1:
                if op.outputs[0].shape.ndims == 4:  # [batch, height, width, channels]
                    input_tensor = op.outputs[0]
                    print(f"Selected input tensor by shape: {op.name}")
                    break

    # Find output tensor
    output_tensor = None
    for name in possible_output_names:
        try:
            output_tensor = graph.get_tensor_by_name(name)
            print(f"Found output tensor: {name}")
            break
        except:
            continue

    if output_tensor is None:
        # Look for softmax or final dense layer
        for op in ops:
            if 'softmax' in op.name.lower() or 'predictions' in op.name.lower():
                output_tensor = op.outputs[0]
                print(f"Selected output tensor by name: {op.name}")
                break

    return input_tensor, output_tensor


def predict_batch(graph, input_tensor, output_tensor, images, batch_size=32):
    """
    Run batch prediction on the loaded model
    """
    predictions = []

    with tf.Session(graph=graph) as sess:
        for i in range(0, len(images), batch_size):
            batch = images[i:i + batch_size]

            # Run inference
            batch_pred = sess.run(output_tensor,
                                  feed_dict={input_tensor: batch})

            # Get predicted class (index with highest probability)
            batch_pred_classes = np.argmax(batch_pred, axis=1)
            predictions.extend(batch_pred_classes)

            if i % (batch_size * 10) == 0:
                print(f"Processed {min(i + batch_size, len(images))}/{len(images)} images")

    return np.array(predictions)


def evaluate_model_comprehensive(model_path, test_images, test_labels, class_names):
    """
    Complete evaluation pipeline
    """
    print("=" * 60)
    print("MODEL EVALUATION REPORT")
    print("=" * 60)

    # 1. Load model
    print("\n1. Loading model...")
    graph = load_frozen_model(model_path)
    input_tensor, output_tensor = get_model_io_tensors(graph)
    print("i/o")
    print(input_tensor, output_tensor)

    if input_tensor is None or output_tensor is None:
        print("ERROR: Could not find input/output tensors.")
        print("\nAvailable tensors in your model:")
        ops = graph.get_operations()
        for i, op in enumerate(ops[:20]):  # Show first 20 ops
            print(f"  {op.name}")
        if len(ops) > 20:
            print(f"  ... and {len(ops) - 20} more")
        return None

    # 2. Run predictions
    print("\n2. Running predictions...")
    predictions = predict_batch(graph, input_tensor, output_tensor, test_images)

    # 3. Calculate metrics
    print("\n3. Calculating metrics...")

    # Basic metrics
    accuracy = accuracy_score(test_labels, predictions)

    # For multi-class, use 'macro' average (treats all classes equally)
    precision = precision_score(test_labels, predictions, average='macro', zero_division=0)
    recall = recall_score(test_labels, predictions, average='macro', zero_division=0)
    f1 = f1_score(test_labels, predictions, average='macro', zero_division=0)

    # Weighted averages (considers class imbalance)
    precision_weighted = precision_score(test_labels, predictions, average='weighted', zero_division=0)
    recall_weighted = recall_score(test_labels, predictions, average='weighted', zero_division=0)
    f1_weighted = f1_score(test_labels, predictions, average='weighted', zero_division=0)

    # 4. Display results
    print("\n" + "=" * 60)
    print("EVALUATION METRICS")
    print("=" * 60)

    print(f"\nOverall Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")

    print("\n--- Macro Averages (equal weight per class) ---")
    print(f"Precision: {precision:.4f}")
    print(f"Recall:    {recall:.4f}")
    print(f"F1 Score:  {f1:.4f}")

    print("\n--- Weighted Averages (weighted by class size) ---")
    print(f"Precision: {precision_weighted:.4f}")
    print(f"Recall:    {recall_weighted:.4f}")
    print(f"F1 Score:  {f1_weighted:.4f}")

    # 5. Detailed classification report
    print("\n" + "=" * 60)
    print("DETAILED CLASS-WISE METRICS")
    print("=" * 60)

    report = classification_report(test_labels, predictions,
                                   target_names=class_names,
                                   zero_division=0)
    print(report)

    # 6. Confusion Matrix
    print("\n" + "=" * 60)
    print("CONFUSION MATRIX")
    print("=" * 60)

    cm = confusion_matrix(test_labels, predictions)

    # Display confusion matrix as text (for quick view)
    print("\nConfusion Matrix (rows: true, columns: predicted):")
    print(f"{'':<15}", end="")
    for i in range(min(10, len(class_names))):
        print(f"{i:<4}", end="")
    print("...")

    for i in range(min(10, len(class_names))):
        print(f"{class_names[i][:12]:<12} |", end="")
        for j in range(min(10, len(class_names))):
            print(f"{cm[i,j]:<4}", end="")
        if len(class_names) > 10:
            print("...", end="")
        print()

    # 7. Return all results for further analysis
    results = {
        'accuracy': accuracy,
        'precision_macro': precision,
        'recall_macro': recall,
        'f1_macro': f1,
        'precision_weighted': precision_weighted,
        'recall_weighted': recall_weighted,
        'f1_weighted': f1_weighted,
        'predictions': predictions,
        'confusion_matrix': cm,
        'class_names': class_names
    }

    return results

import seaborn as sns
def visualize_results(results, save_dir='./evaluation_results'):
    """
    Create visualizations of the evaluation results
    """
    os.makedirs(save_dir, exist_ok=True)

    # 1. Confusion Matrix Heatmap
    plt.figure(figsize=(12, 10))
    cm = results['confusion_matrix']
    class_names = results['class_names']

    # Normalize confusion matrix
    cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

    sns.heatmap(cm_normalized, annot=True, fmt='.2f', cmap='Blues',
                xticklabels=class_names, yticklabels=class_names)
    plt.title('Normalized Confusion Matrix')
    plt.xlabel('Predicted Label')
    plt.ylabel('True Label')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, 'confusion_matrix.png'), dpi=150)
    plt.show()

    # 2. Metrics Bar Chart
    plt.figure(figsize=(10, 6))
    metrics = ['Accuracy', 'Precision\n(Macro)', 'Recall\n(Macro)', 'F1 Score\n(Macro)']
    values = [results['accuracy'], results['precision_macro'],
              results['recall_macro'], results['f1_macro']]

    colors = ['skyblue', 'lightgreen', 'lightcoral', 'gold']
    bars = plt.bar(metrics, values, color=colors, edgecolor='black')

    # Add value labels on top of bars
    for bar, value in zip(bars, values):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2., height + 0.01,
                 f'{value:.3f}', ha='center', va='bottom')

    plt.ylim(0, 1.1)
    plt.title('Model Evaluation Metrics')
    plt.ylabel('Score')
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, 'metrics_summary.png'), dpi=150)
    plt.show()

    # 3. Save results to file
    with open(os.path.join(save_dir, 'evaluation_report.txt'), 'w') as f:
        f.write("MODEL EVALUATION REPORT\n")
        f.write("=" * 50 + "\n\n")

        f.write(f"Test Dataset Size: {len(results.get('predictions', []))}\n")
        f.write(f"Number of Classes: {len(class_names)}\n")
        f.write(f"Classes: {', '.join(class_names)}\n\n")

        f.write("OVERALL METRICS:\n")
        f.write("-" * 30 + "\n")
        f.write(f"Accuracy:           {results['accuracy']:.4f}\n")
        f.write(f"Precision (Macro):  {results['precision_macro']:.4f}\n")
        f.write(f"Recall (Macro):     {results['recall_macro']:.4f}\n")
        f.write(f"F1 Score (Macro):   {results['f1_macro']:.4f}\n\n")

        f.write("CONFUSION MATRIX:\n")
        f.write("-" * 30 + "\n")
        for i, row in enumerate(cm):
            f.write(f"{class_names[i][:15]:<15}: {row}\n")

def evaluate_model(request):
    # Configuration
    MODEL_PATH = r"C:\Users\isasu\Music\project\web\D_daignosis\myapp\new_logs\output_graph.pb"  # Your trained model
    TEST_DATA_DIR = r"C:\Users\isasu\Music\project\web\D_daignosis\myapp\static\mri validation"  # Your test data

    # Step 1: Load test data
    print("Loading test dataset...")
    test_images, test_labels, class_names, image_paths = load_test_dataset_from_folders(
        TEST_DATA_DIR,
        img_size=(224, 224)  # Adjust to your model's expected input size
    )

    if len(test_images) == 0:
        print("ERROR: No test images loaded. Check your directory path.")
        return

    # Step 2: Evaluate model
    results = evaluate_model_comprehensive(
        MODEL_PATH,
        test_images,
        test_labels,
        class_names
    )

    if results is not None:
        # Step 3: Visualize results
        print("\nGenerating visualizations...")
        visualize_results(results)

        # Step 4: Show some example predictions
        print("\n" + "=" * 60)
        print("SAMPLE PREDICTIONS")
        print("=" * 60)

        # Show first 10 predictions
        for i in range(min(10, len(image_paths))):
            true_class = class_names[test_labels[i]]
            pred_class = class_names[results['predictions'][i]]
            correct = "✓" if test_labels[i] == results['predictions'][i] else "✗"

            print(f"{correct} {os.path.basename(image_paths[i]):<30} "
                  f"True: {true_class:<15} Predicted: {pred_class:<15}")

    return render(request, "admin/evaluation.html")





####################        experts

def doctor_signup(request):
    return render(request,'doctor/signup_index.html')

def doctor_signup_post(request):
    name=request.POST['textfield']
    email=request.POST['textfield2']
    phone_number=request.POST['textfield4']
    photo=request.FILES['textfield6']
    qualification=request.POST['textfield7']
    proof=request.FILES['textfield8']
    password=request.POST['textfield10']

    from datetime import datetime
    date=datetime.now().strftime("%Y%m%d-%H%M%S")+'-1.jpg'
    fs=FileSystemStorage()
    fn=fs.save(date,photo)
    path=fs.url(date)

    from datetime import datetime
    date1=datetime.now().strftime("%Y%m%d-%H%M%S")+'-2.jpg'
    fs1=FileSystemStorage()
    fn1=fs1.save(date1,proof)
    path1=fs1.url(date1)

    user=User.objects.create(username=email,password=make_password(password))
    user.groups.add(Group.objects.get(name="expert"))
    user.save()

    ob=Expert()
    ob.name=name
    ob.email=email
    ob.phonenumber=phone_number
    ob.photo=path
    ob.qualification=qualification
    ob.proof=path1
    ob.AUTHUSER=user
    ob.status='pending'
    ob.save()
    messages.success(request,"Registered Successfull")
    return redirect("/myapp/login_get/")


def doctornhome(request):
    return render(request,'doctor/homeindex.html')


def doctor_profile(request):
    variable=Expert.objects.get(AUTHUSER_id=request.user.id)
    return render(request,'doctor/view profile.html',{'data':variable})

def doctor_edit_profile(request):
    ob = Expert.objects.get(AUTHUSER=request.user.id)
    return render(request,'doctor/doctor edit priofile.html',{'data':ob})

def doctor_edit_profile_post(request):
    name=request.POST['textfield']
    phone_number=request.POST['textfield4']
    qualification=request.POST['textfield7']
    ob = Expert.objects.get(AUTHUSER_id=request.user.id)

    if 'photo' in request.FILES:
        photo = request.FILES['photo']
        from datetime import datetime
        date = datetime.now().strftime("%Y%m%d-%H%M%S") + '.jpg'
        fs = FileSystemStorage()
        fn = fs.save(date, photo)
        path = fs.url(date)
        ob.photo=path

        # return HttpResponse('''<script>alert('success');window.location='/myapp/doctor_profile/'</script>''')
    if 'proof' in request.FILES:
        proof = request.FILES['proof']
        from datetime import datetime
        date1 = datetime.now().strftime("%Y%m%d-%H%M%S") + '.jpg'
        fs1 = FileSystemStorage()
        fn1 = fs1.save(date1, proof)
        path1 = fs1.url(date1)
        ob.proof=path1
    ob.name=name
    ob.phonenumber=phone_number
    ob.qualification=qualification
    ob.save()
    messages.success(request,"Updated Successfully")
    return redirect("/myapp/doctor_profile/")


def doctor_REVIEW(request):
    variable=Review.objects.filter(EXPERT__AUTHUSER_id=request.user.id)
    return render(request,'doctor/VIEW REVIEW.html',{'data':variable})


def doctor_REVIEW_post(request):
    FROM = request.POST['textfield']
    TO = request.POST['textfield2']

    variable = Review.objects.filter(EXPERT__AUTHUSER_id=request.user.id,Date__range=[FROM,TO])
    return render(request, 'doctor/VIEW REVIEW.html', {'data': variable})



def doctor_change_password(request):
    return render(request,'doctor/change password.html')

def doctor_change_password_post(request):
    current_password=request.POST['textfield']
    new_password=request.POST['textfield2']
    confirm_password=request.POST['textfield3']
    user = request.user
    if not user.check_password(current_password):
        return HttpResponse("<script>alert('Invalid password'); window.location='/myapp/doctor_change_password';</script>")
    if new_password == confirm_password:
        user.set_password(confirm_password)
        user.save()
        return HttpResponse("<script>alert('Password changed'); window.location='/myapp/login_get';</script>")
    else:
        return HttpResponse("<script>alert('Password mismatch'); window.location='/myapp/doctor_change_password';</script>")

def doctor_add_schedule(request):
    return render(request, "doctor/Manage schedule.html")
def doctor_add_schedule_post(request):
    date=request.POST['schedule_date']
    from_time=request.POST['from_time']
    to_time=request.POST['to_time']
    obj=Schedule()
    obj.scheduledate=date
    obj.fromtime=from_time
    obj.totime=to_time
    obj.EXPERT=Expert.objects.get(AUTHUSER_id=request.user.id)
    obj.save()
    return HttpResponse("<script>alert('Schedule added'); window.location='/myapp/doctor_schedule';</script>")


def doctor_schedule(request):
    variable=Schedule.objects.filter(EXPERT__AUTHUSER_id=request.user.id)
    return render(request,'doctor/VIEW SCHEDULE.html',{'data':variable})

def delete_schedule(request, id):
    Schedule.objects.filter(id=id).delete()
    return HttpResponse("<script>alert('Schedule deleted'); window.location='/myapp/doctor_schedule';</script>")


#
def doctor_appoiment(request):
    variable=Appointment.objects.filter(SCHEDULE__EXPERT__AUTHUSER_id=request.user.id)
    return render(request,'doctor/view appoiment.html',{'data':variable})


def doctor_appoinment_post(request):
    FROM=request.POST['textfield']
    TO=request.POST['textfield2']
    variable=Appointment.objects.filter(EXPERT__AUTHUSER_id=request.user.id,Date__range=[FROM,TO])
    return render(request,'doctor/view appoiment.html',{'data':variable})

def doc_upload(request, id):
    return render(request, "doctor/prediction.html", {"id":id})

def doc_upload_post(request, id):
    img_file=request.FILES['filefield']
    aud_file=request.FILES['filefield2']

    dt=datetime.now().strftime("%Y%m%d_%H%M%S")

    file_path1=r"C:\Users\isasu\Music\project\web\D_daignosis\media\\"+dt+"_img.jpg"
    file_path2=r"C:\Users\isasu\Music\project\web\D_daignosis\media\\"+dt+"_aud.wav"

    fs=FileSystemStorage()
    fs.save(file_path1, img_file)
    fs.save(file_path2, aud_file)

    pred1, score1=check(file_path1)
    pred2 = predict_audio(file_path2)

    #   old code
    # if pred1 == "pd patients" and pred2 == "PD":
    #     stat="Parkinsons"
    # else:
    #     stat = "Healthy"


    #       FOR FUSED
    if pred1 == "pd patients":
        p_mri = 1
    else:
        p_mri = 0
    if pred2 == "PD":
        p_voice = 1
    else:
        p_voice = 0
    try:
        denom=(p_voice*p_mri)+((1-p_voice)*(1-p_mri))
        p_fused = (p_voice*p_mri)/denom
    except Exception as e:
        p_fused=0
    print("Fused result :", p_fused)

    if p_fused == 1:
        stat = "Parkinsons"
    else:
        stat = "Healthy"
    obj=Prediction()
    obj.APPOINTMENT_id=id
    obj.Prediction=stat
    obj.Date=datetime.now().date()
    obj.Filepath1="/media/"+dt+"_img.jpg"
    obj.Filepath2="/media/"+dt+"_aud.wav"
    obj.save()

    app_obj=Appointment.objects.get(id=id)
    print("Date", datetime.now().date())
    print("Doctor", app_obj.SCHEDULE.EXPERT.name)
    print("Patient", app_obj.PATIENT.name)
    print("Based on mri", p_mri)
    print("Based on voice", p_voice)
    print("Final fused prediction", p_fused)

    # Generate detailed report
    report_data = {
        'date': datetime.now().date(),
        'doctor':  app_obj.SCHEDULE.EXPERT.name,
        'patient':  app_obj.PATIENT.name,
        'patient_id':  app_obj.PATIENT.id,
        'mri': p_mri,
        'voice': p_voice,
        'final': p_fused
    }

    detailed_filename = f"Detailed_Medical_Report_{report_data['patient_id']}.pdf"
    success = create_detailed_medical_report(detailed_filename, report_data)
    report_path="/media/"+detailed_filename
    return render(request, "doctor/prediction.html", {"id": id, "report_path":report_path, "pred1":pred1, "pred2":pred2, "stat":stat})



# def doctor_schedule(request):
#     v=Schedule.objects.filter(DOCTOR__AUTHUSER__id=request.user.id)
#     return render(request,'doctor/VIEW SCHEDULE.html',{'data':v})
#
#
# def doctor_SCHEDULE_post(request):
#     FROM_DATE = request.POST['textfield']
#     TO = request.POST['textfield2']
#
#     v=Schedule.objects.filter(DOCTOR__LOGIN=request.session['lid'],scheduledate__range=[FROM_DATE,TO])
#     return render(request,'doctor/VIEW SCHEDULE.html',{'data':v})
#
#
#
#
#
# def doc_view_doctor(request):
#     v=Disease.objects.all()
#     return render(request,'doctor/view disease.html',{'data':v})
#
# def delete_schedule(request,id):
#     res=Schedule.objects.filter(id=id).delete()
#     messages.success(request,"Deleted Successfully")
#     return redirect('/myapp/doctor_schedule/')
#
# def edit_schedule(request,id):
#     res=Schedule.objects.get(id=id)
#     return render(request,'doctor/edit schedule.html',{'data':res})
#
# def edit_schedule_post(request):
#     id=request.POST['id']
#     schedule_date=request.POST['schedule_date']
#     from_time=request.POST['from_time']
#     to_time=request.POST['to_time']
#     obj=Schedule.objects.get(id=id)
#     obj.fromtime=from_time
#     obj.totime=to_time
#     obj.scheduledate=schedule_date
#     # obj.DOCTOR=Doctor.objects.get(LOGIN_id=request.session['lid'])
#     obj.save()
#     messages.success(request,"Updated Successfully")
#     return redirect('/myapp/doctor_schedule/')
#

def doctor_predict_result(request):
    return render(request,"doctor/predict.html")
def doctor_predict_result_post(request):
    photo=request.FILES['files']
    fs = FileSystemStorage()
    from datetime import datetime
    date = "p1" + datetime.now().strftime("%Y%m%d-%H%M%S") + ".jpg"
    fn = fs.save(date, photo)
    path = fs.url(date)
    from myapp.classify import check
    pred = check(r"D:\project\web\D_daignosis\\"+path)
    print("Final : ", pred)
    return  render(request,"doctor/predict.html",{'pred':str(pred[0])})

def doctor_predict_result_voice(request):
    return render(request,"doctor/predict_voice.html")
def doctor_predict_result_voice_post(request):
    photo=request.FILES['files']
    fs = FileSystemStorage()
    from datetime import datetime
    date = "p1" + datetime.now().strftime("%Y%m%d-%H%M%S") + ".wav"
    fn = fs.save(date, photo)
    path = fs.url(date)
    pred = predict_audio(r"D:\project\web\D_daignosis\\"+path)
    print("Final : ", pred)
    return  render(request,"doctor/predict_voice.html",{'pred':str(pred)})







#############################       user
def and_login(request):
    username= request.POST['name']
    password= request.POST['password']
    print(username, password)
    usr = authenticate(request, username=username, password=password)
    if usr is not None:
        if usr.groups.filter(name="patient").exists():
            uu=Patient.objects.get(AUTHUSER__id=usr.id)
            return JsonResponse({"status":"ok","lid":str(usr.id),"uname":uu.name,"uphoto":"/media/def_user.png","uemail":uu.email})
        else:
            return JsonResponse({"status":"ohno"})
    else:
        return JsonResponse({"status": "no"})


def and_signup(request):
    name= request.POST['name']
    email= request.POST['email']
    phonenumber= request.POST['phonenumber']
    password= request.POST['password']
    confirmpassword=request.POST['confirmpassword']
    if password == confirmpassword:
        user = User.objects.create(username=email, password=make_password(confirmpassword))
        user.groups.add(Group.objects.get(name="patient"))
        user.save()

        obj=Patient()
        obj.name=name
        obj.email=email
        obj.phonenumber=phonenumber
        obj.AUTHUSER=user
        obj.save()
        return JsonResponse({'status':'ok'})
    else:
        return JsonResponse({'status': 'no'})

def and_view_profile(request):
    lid=request.POST['lid']
    v=Patient.objects.get(AUTHUSER_id=lid)
    return JsonResponse({'status':'ok','name':v.name,'email':v.email,'phonenumber':v.phonenumber})

def user_view_doctor(request):
    ress = Expert.objects.filter(status='approved')
    l = []
    for i in ress:
        l.append({'id': i.id, 'name': i.name, 'dlid': i.AUTHUSER.id, 'email': i.email, 'phoneno': i.phonenumber,
                  'qualification': i.qualification, 'photo': i.photo})
    return JsonResponse({'status': 'ok', 'data': l})

# def chat1(request,id):
#     request.session["userid"] = id
#     cid = str(request.session["userid"])
#     request.session["new"] = cid
#     qry = Patient.objects.get(AUTHUSER__id=cid)
#     return render(request, "doctor/Chat.html", {'photo': qry.photo, 'name': qry.name, 'toid': cid})
#
# def chat_view(request):
#     fromid = request.user.id
#     toid = request.session["userid"]
#     qry = Patient.objects.get(AUTHUSER__id=request.session["userid"])
#     from django.db.models import Q
#     res = Chat.objects.filter(Q(FROMID_id=fromid, TOID_id=toid) | Q(FROMID_id=toid, TOID_id=fromid))
#     l = []
#
#     for i in res:
#         l.append({"id": i.id, "message": i.message, "to": i.TOID_id, "date": i.date, "from": i.FROMID_id})
#
#     return JsonResponse({'photo': qry.photo, "data": l, 'name': qry.name, 'toid': request.session["userid"]})
#
# def chat_send(request, msg):
#     lid = request.user.id
#     toid = request.session["userid"]
#     message = msg
#
#     import datetime
#     d = datetime.datetime.now().date()
#     chatobt = Chat()
#     chatobt.message = message
#     chatobt.TOID_id = toid
#     chatobt.FROMID_id = lid
#     chatobt.date = d
#     chatobt.save()
#
#     return JsonResponse({"status": "ok"})
#
#
#
#
def User_sendchat(request):
    FROM_id=request.POST['from_id']
    TOID_id=request.POST['to_id']
    msg=request.POST['message']

    from  datetime import datetime
    c=Chat()
    c.EXPERT=Expert.objects.get(AUTHUSER_id=TOID_id)
    c.USER=Patient.objects.get(AUTHUSER_id=FROM_id)
    c.message=msg
    c.date=datetime.now()
    c.Type="user"
    c.save()
    return JsonResponse({'status':"ok"})
#
#
def User_viewchat(request):
    fromid = request.POST["from_id"]
    toid = request.POST["to_id"]

    exp=Expert.objects.get(AUTHUSER_id=toid)
    res = Chat.objects.filter(EXPERT_id=exp, USER__AUTHUSER_id=fromid)
    l = []

    for i in res:
        l.append({"id": i.id, "msg": i.message, "type": i.Type, "date": i.date})

    return JsonResponse({"status":"ok",'data':l})
#


def and_changepassword(request):
    lid=request.POST['lid']
    current_password=request.POST['current']
    new_password=request.POST['new_password']
    confirm_password=request.POST['confirm']
    user = User.objects.get(id=lid)
    if not user.check_password(current_password):
        return JsonResponse({"status":"no"})
    user.set_password(confirm_password)
    user.save()
    return JsonResponse({"status":"ok"})

#
#
#
# def and_edit_profile(request):
#     lid=request.POST['lid']
#     name= request.POST['name']
#     email= request.POST['email']
#     phonenumber= request.POST['phone']
#     place= request.POST['place']
#     pin= request.POST['pin']
#     post= request.POST['post']
#     photo= request.POST['photo']
#     gender=request.POST['gender']
#
#     if len(photo)>5:
#         from datetime import datetime
#         date = datetime.now().strftime('%Y%m%d-%H%M%S') + '.jpg'
#         import base64
#         a = base64.b64decode(photo)
#         fh = open(r"D:\project\web\D_daignosis\media\user\\" + date, "wb")
#         path = '/media/user/' + date
#         fh.write(a)
#         fh.close()
#         obj=Patient.objects.get(AUTHUSER_id=lid)
#         obj.photo=path
#         obj.save()
#     obj = Patient.objects.get(AUTHUSER_id=lid)
#     obj.name = name
#     obj.email = email
#     obj.phonenumber = phonenumber
#     obj.place = place
#     obj.pin = pin
#     obj.post = post
#
#     obj.gender = gender
#     obj.save()
#
#     log = User.objects.get(id=lid)
#     log.username = email
#     log.save()
#     return JsonResponse({'status':'ok'})


def and_view_doctor(request):
    res = Expert.objects.all()
    l = []
    for i in res:
        l.append({'id':i.id, "dlid":i.AUTHUSER.id,'name':i.name, 'email':i.email,'phoneno':i.phonenumber,
                  'qualification':i.qualification, "photo":i.photo})
    return JsonResponse({'status':'ok','data':l})


#
# def and_user_edit_profile(request):
#     id = request.POST['lid']
#     name = request.POST['name']
#     dob = request.POST['dob']
#     place = request.POST['place']
#     post = request.POST['post']
#     pin = request.POST['pin']
#     housename = request.POST['hname']
#     district = request.POST['district']
#     gender = request.POST['gender']
#     email = request.POST['email']
#     phoneno = request.POST['phone']
#     photo = request.POST['photo']
#     if photo > str(0):
#         import time, datetime
#         from encodings.base64_codec import base64_decode
#         import base64
#
#         # fs=FileSystemStorage()
#         timestr = time.strftime("%Y%m%d-%H%M%S")
#         # fn=fs.save(photo,timestr)
#         #print(timestr)
#         a = base64.b64decode(photo)
#         fh = open(r"D:\project\web\D_daignosis\media\user\\" + timestr + ".jpg", "wb")
#         path = "/media/user/" + timestr + ".jpg"
#         fh.write(a)
#         fh.close()
#         res = User.objects.filter(LOGIN__id=id).update(name=name, dob=dob, place=place, post=post, pin=pin,
#                                                  gender=gender, email=email, phonenumber=phoneno,
#                                                 photo=photo)
#     else:
#         res=User.objects.filter(LOGIN__id=id).update(name=name,dob=dob,place=place,post=post,pin=pin,gender=gender,email=email,phonenumber=phoneno)
#     return JsonResponse({'status':"ok"})



def view_user_schedule(request):
    did=request.POST['did']
    ress=Schedule.objects.filter(EXPERT_id=did)
    l=[]
    for i in ress:
        l.append({'id':i.id,'fromtime':i.fromtime,'totime':i.totime,'date':i.scheduledate})
    return JsonResponse({'status':'ok','data':l})


def view_user_reviews(request):
    did=request.POST['did']
    ress=Review.objects.filter(EXPERT_id=did)
    l=[]
    for i in ress:
        l.append({'id':i.id,'date':i.Date,'review':i.review,
                  'patient':i.PATIENT.name+"\n"+i.PATIENT.email})
    return JsonResponse({'status':'ok','data':l})

#
def and_user_take_appointment(request):
    sid=request.POST['sid']
    lid=request.POST['lid']

    uu=Patient.objects.get(AUTHUSER__id=lid)
    from datetime import datetime

    data=Appointment.objects.filter(SCHEDULE_id=sid, PATIENT=uu, Date=datetime.now().today())
    if data.exists():
        return JsonResponse({'status':"no"})


    aobj=Appointment()
    aobj.Date=datetime.now().today()
    aobj.SCHEDULE_id=sid
    aobj.PATIENT=uu
    aobj.Status="pending"
    aobj.save()
    return JsonResponse({'status':"ok"})

def and_user_view_appointment(request):
    lid=request.POST['lid']
    ress=Appointment.objects.filter(PATIENT__AUTHUSER__id=lid)
    l=[]
    for i in ress:
        l.append({'id':str(i.id),
                  'dname':i.SCHEDULE.EXPERT.name,
                  'dphone':str(i.SCHEDULE.EXPERT.phonenumber),
                  'dlid':str(i.SCHEDULE.EXPERT.AUTHUSER.id),
                  'did':str(i.SCHEDULE.EXPERT.id),
                  "date":i.Date.strftime("%Y-%m-%d"),
                  "sched":i.SCHEDULE.scheduledate + "("+i.SCHEDULE.fromtime +"-"+i.SCHEDULE.totime+")"})
    print(l)
    return JsonResponse({'status':"ok",'data':l})
#
# # def and_user_send_question(request):
# #     lid=request.POST['lid']
# #     qstn=request.POST['question']
# #     uu=user.objects.get(LOGIN__id=lid)
# #     dd=question()
# #     dd.questions=qstn
# #     dd.date=datetime.datetime.now()
# #     dd.USER=uu
# #     dd.save()
# #     return JsonResponse({"status":"ok"})
# #
# # def and_user_view_comments(request):
# #     lid=request.POST['lid']
# #     ress=comments.objects.filter(QUESTION__USER__LOGIN__id=lid)
# #     l=[]
# #     for i in ress:
# #         l.append({"id":i.id,"question":i.QUESTION.questions,"date":i.date,"comments":i.comment})
# #     return JsonResponse({"status":"ok","data":l})
#
#
def and_send_complaint(request):
    lid=request.POST['lid']
    did=request.POST['did']
    comp=request.POST['complaint']
    cc=Complaint()
    cc.complaint=comp
    from datetime import datetime
    cc.Date=datetime.now().today()
    cc.reply="pending"
    cc.status="pending"
    cc.PATIENT=Patient.objects.get(AUTHUSER__id=lid)
    cc.EXPERT=Expert.objects.get(id=did)
    cc.save()
    return JsonResponse({"status":"ok"})

def and_view_complaint_reply(request):
    lid=request.POST['lid']
    did=request.POST['did']
    ress=Complaint.objects.filter(PATIENT__AUTHUSER__id=lid,DOCTOR_id=did)
    l=[]
    for i in ress:
        l.append({"id":i.id,"complaint":i.complaint,"date":i.Date,"reply":i.reply,"status":i.status,'dname':i.EXPERT.name})
    return JsonResponse({"status":"ok","data":l})
#
#
def and_user_send_feedback(request):
    lid=request.POST['lid']
    d=request.POST['did']
    feed=request.POST['feedback']

    ff=Review()
    ff.review=feed
    from datetime import datetime
    ff.Date=datetime.now().today()
    ff.PATIENT=Patient.objects.get(AUTHUSER__id=lid)
    ff.EXPERT=Expert.objects.get(id=d)
    ff.save()
    return JsonResponse({"status":"ok"})
#
#
# def upload_image(request):
#     photo=request.FILES['photo']
#
#     date=datetime.now().strftime("%Y%m%d%H%M%S")+".jpg"
#     fs=FileSystemStorage()
#     date = "p1" + datetime.now().strftime("%Y%m%d-%H%M%S") + ".jpg"
#     fn = fs.save(date, photo)
#     path = fs.url(date)
#     from myapp.classify import check
#     pred = check(r"D:\project\web\D_daignosis\\" + path)
#     return JsonResponse({"status":"ok","name":str(pred[0])})
#
# def upload_audio(request):
#     photo=request.FILES['audiofile']
#
#     date=datetime.now().strftime("%Y%m%d%H%M%S")+".wav"
#     fs=FileSystemStorage()
#     # date = "p1" + datetime.now().strftime("%Y%m%d-%H%M%S") + ".jpg"
#     fn = fs.save(date, photo)
#     path = fs.url(date)
#     from myapp.voice_pred import predict_audio
#     pred = predict_audio(r"D:\project\web\D_daignosis\\" + path)
#     return JsonResponse({"status":"ok","prediction":str(pred)})
#
