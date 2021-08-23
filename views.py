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

    result_list = []
    for i in range(target_sim.shape[1]):
        result_list.append([])
        result_list[i].append(target_sim.columns[i])
        result_list[i].append(list(target_sim.iloc[:, i].nlargest(5).index))
        result_list[i].append(list(target_sim.iloc[:, i].nlargest(5)))

    session['result_list'] = result_list

    return redirect("/result")


@app.route("/result")
def result():
    result_list = session['result_list']

    return render_template("result.html", page_title="predict result", result_list=result_list, active="")

@app.route("/job_history")
def job_history():
    return render_template("job_history.html", page_tiel="PSnoD jobs", active="job_history")

@app.route("/info")
def info():
    return render_template("infomation.html", page_tiel="PSnoD info", active="infomation")

@app.route("/download_seq")
def download_seq():
    with open("./static/data/snoRNA_seq_noID.fa", "r") as f:
        seq_file = f.read()
    return Response(seq_file, mimetype="text/plain")