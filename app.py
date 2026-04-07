from flask import Flask, render_template, request, redirect
import io
import base64
import matplotlib.pyplot as plt

app = Flask(__name__)

# Temporary storage
expenses = []

@app.route('/')
def index():
    total = sum(e['amt'] for e in expenses)

    # Category totals
    cat_totals = {}
    for e in expenses:
        cat_totals[e['cat']] = cat_totals.get(e['cat'], 0) + e['amt']

    # Generate pie chart
    chart = None
    if cat_totals:
        fig, ax = plt.subplots()
        ax.pie(
            cat_totals.values(),
            labels=cat_totals.keys(),
            autopct='%1.1f%%'
        )
        ax.set_title('Category Breakdown')

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        chart = base64.b64encode(buf.getvalue()).decode()
        plt.close(fig)

    return render_template('index.html',
                           expenses=expenses,
                           total=total,
                           chart=chart)


@app.route('/add', methods=['POST'])
def add():
    desc = request.form.get('desc')
    amt = request.form.get('amt')
    cat = request.form.get('cat')

    if desc and amt:
        expenses.append({
            'desc': desc,
            'amt': float(amt),
            'cat': cat
        })

    return redirect('/')


@app.route('/delete/<int:id>')
def delete(id):
    if 0 <= id < len(expenses):
        expenses.pop(id)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)