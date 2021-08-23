from main import *
from help_functions import *
from predictor import *


@app.route("/")
def index():
    return render_template("index.html", page_title="PSnoD", active="")

@app.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "GET":
        return render_template("predict.html", page_tiel="PSnoD predict", active="predict")

    user_folder_path = os.path.join(app.config['UPLOAD_FOLDER'], "uid_1")

    textarea = request.form["inputed_sequence"]

    if textarea != "":
        user_fasta_list = read_fasta_from_str(textarea)
    else:
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(user_folder_path, filename))
            user_fasta_list = read_fasta_from_file(os.path.join(user_folder_path, filename))
        else:
            flash('Not Allowed filename!')
            return redirect(request.url)
    if len(user_fasta_list) < 1:
        return redirect(request.url)

    target_sim = predict_snoRNAs(user_fasta_list)
    target_sim.to_csv(os.path.join(user_folder_path, "job1.csv"))

    result_dict = []
    for i in range(target_sim.shape[1]):
        result_dict.append([])
        result_dict[i].append(target_sim.columns[i])
        result_dict[i].append(list(target_sim.iloc[:, i].nlargest(5).index))
        result_dict[i].append(list(target_sim.iloc[:, i].nlargest(5)))

    return render_template("result.html", page_title="predict result", result_dict=result_dict, active="")


@app.route("/job_history")
def job_history():
    return render_template("job_history.html", page_tiel="PSnoD jobs", active="job_history")