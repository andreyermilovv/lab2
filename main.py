from tkinter import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint


class Parameter:
    def __init__(self, index, label, funcs, faks):
        self.index = index
        self.label = label
        self.b = []
        self.b_fak = []
        self.d_fak = []
        self.d = []
        self.funcs = {}
        for ind, f in enumerate(funcs):
            if f == 1:
                self.b.append("m" + str(ind + 1))
            elif f == -1:
                self.d.append("m" + str(ind + 1))

        for ind, fak in enumerate(faks):
            if fak == 1:
                self.b_fak.append("FaK" + str(ind + 1))
            elif fak == -1:
                self.d_fak.append("FaK" + str(ind + 1))

    def calculate(self, max_val, funcs, faks):
        res_b_f = list(map(lambda x: funcs[self.funcs[x]], self.b))
        res_d_f = list(map(lambda x: funcs[self.funcs[x]], self.d))

        res_b_fak = list(map(lambda x: faks[x], self.b_fak))
        res_d_fak = list(map(lambda x: faks[x], self.d_fak))

        return lambda y, t: 1 / max_val * (np.prod(list(map(lambda x: x(t), res_b_f))) * sum(
            list(map(lambda x: x(t), res_b_fak))) - np.prod(list(map(lambda x: x(t), res_d_f))) * sum(
            list(map(lambda x: x(t), res_d_fak))))


max_m = [1 for i in range(10)]
excel_file_path = 'lab2.xlsx'
chars = pd.read_excel(excel_file_path)
excel_rows = chars.values
characteristics_labels = [col_name.replace('\n', '') for col_name in chars.columns[1:]]
char_faks_index = characteristics_labels.index('Fak1')
table = {}
params = []
for index_row, excel_row in enumerate(excel_rows):
    name = excel_row[0]
    table[name] = {}

    for i, cell in enumerate(excel_row[1:]):
        table[name][characteristics_labels[i]] = cell

    char_val = list(table[name].values())
    params.append(Parameter(index_row + 1, name, char_val[:char_faks_index],
                            char_val[char_faks_index:]))

func_m = {}
for i in params:
    for f in (i.b + i.d):
        name = 'f' + str(len(func_m.keys()) + 1)
        func_m[name] = lambda t: 1
        i.funcs[f] = name


def f9(t, a1, a2, a3):
    return float(a1) * np.array(t) ** 3 + float(a2)


def f10(t, a1, a2, a3):
    return float(a1) * t + float(a2)


def f37(t, a1, a2, a3):
    return float(a1) * t + float(a2)


def f78(t, a1, a2, a3):
    return float(a1) * t ** 2 + float(a2) * t + float(a3)


def f88(t, a1, a2, a3):
    return float(a1) * t ** 2 + float(a2) * t + float(a3)


def fak1(t):
    return -t ** 3 + 0.8


def fak2(t):
    return np.cos(1.5 * t) ** 2 / 2 + 0.2


def fak3(t):
    res = np.where(t < 0, -1, t)
    res = np.where(t > 1, -1, res)
    res = np.where(t <= 1, 0.9, res)
    res = np.where(t <= 0.7, 0.8, res)
    res = np.where(t <= 0.2, 0.5, res)
    return res


def fak4(t):
    return np.sin(9 * t) * np.sin(5 * t) * 0.3 + 0.5


def fak5(t):
    return np.sqrt(t) * 0.5 + 0.3


def fak6(t):
    return np.sin(t) * 0.5 + 0.7


fak_f = {'FaK1': fak1, 'FaK2': fak2, 'FaK3': fak3, 'FaK4': fak4, 'FaK5': fak5, 'FaK6': fak6}
res = {}


def calculate():
    func_m['f'+spin1.get()] = lambda te: 1
    func_m['f'+spin2.get()] = lambda t: f10(t, a01v.get(), a11v.get(), a21v.get())
    func_m['f'+spin3.get()] = lambda t: f37(t, a02v.get(), a12v.get(), a22v.get())
    func_m['f'+spin4.get()] = lambda t: f78(t, a03v.get(), a13v.get(), a23v.get())
    func_m['f'+spin5.get()] = lambda t: f88(t, a04v.get(), a14v.get(), a24v.get())
    init_params = [float(m0v.get()), float(m1v.get()), float(m2v.get()), float(m3v.get()), float(m4v.get()),
                   float(m5v.get()), float(m6v.get()), float(m7v.get()), float(m8v.get()), float(m9v.get())]
    for i, char in enumerate(params):
        t = np.linspace(0, 1, 110)  # vector of time
        y0 = 1  # start value
        m_c = char.calculate(max_m[i], func_m, fak_f)
        init_m_param = float(init_params[i])
        y = odeint(m_c, init_m_param, t)  # solve eq.
        y = np.array(y).flatten()
        res[char.label] = y
    print(res)


def get_faks_image():
    fig = plt.subplots()
    t = np.linspace(0, 1, 100)

    plt.plot(t, fak1(t))
    plt.plot(t, fak2(t))
    plt.plot(t, fak3(t))
    plt.plot(t, fak4(t))
    plt.plot(t, fak5(t))
    plt.plot(t, fak6(t))

    # показываем график

    plt.ylim([0, 1])
    plt.legend(['FaK1', 'FaK2', 'FaK3', 'FaK4', 'FaK5', 'FaK6'], bbox_to_anchor=(1, 1))
    plt.xlabel("Время", fontsize=15, color="black")
    plt.ylabel("Возмущения", fontsize=15, color="black")
    plt.show()
    fig[0].tight_layout()
    fig[0].savefig('fak.png')


def make_radar_chart(name, stats, attribute_labels, plot_markers=[0, 0.2, 0.4, 0.6, 0.8, 1],
                     plot_str_markers=["0", "0.2", "0.4", "0.6", "0.8", "1"]):
    labels = np.array(attribute_labels)
    labels[2] = 'Соперничество стран'
    labels[3] = 'Напряженность между США и Китаем               '
    labels[7] = 'Падение экономики Ближнего Востока                                         '
    labels[8] = '        Уход Ангелы Меркель'
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False)
    stats = np.concatenate((stats, [stats[0]]))
    angles = np.concatenate((angles, [angles[0]]))

    init_params = [float(m0v.get()), float(m1v.get()), float(m2v.get()), float(m3v.get()), float(m4v.get()),
                   float(m5v.get()), float(m6v.get()), float(m7v.get()), float(m8v.get()), float(m9v.get())]
    init_params = np.concatenate((init_params, [init_params[0]]))
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, polar=True)
    ax.plot(angles, stats, 'o-', linewidth=2)
    ax.fill(angles, stats, alpha=0.25)
    ax.plot(angles, init_params, 'o-', linewidth=2)
    ax.fill(angles, init_params, alpha=0)
    ax.set_thetagrids(angles[:-1] * 180 / np.pi, labels)
    plt.yticks(plot_markers)
    ax.set_title(name)
    ax.grid(True)
    plt.tight_layout()
    fig.savefig("diag.png")

    return plt.show()


def get_diag():
    labels = list(res.keys())
    t_110 = np.linspace(0, 1, 110)
    res_index = 0
    for i, t_i in enumerate(t_110):
        if t_i > float(diagTv.get()):
            break
        res_index = i
    stats = [i[res_index] for i in res.values()]
    make_radar_chart('T=' + diagTv.get(), stats, labels)


def get_graphics():
    fig = plt.figure(figsize=(10, 5))

    t = np.linspace(0, 1, 110)

    legend_labels = []
    for i in range(10):
        plt.plot(t, res[params[i].label], linewidth=1)
        legend_labels.append(params[i].label)
    plt.xlim([0, 1])
    plt.ylim([0, 1])
    plt.legend(legend_labels, bbox_to_anchor=(1, 1))
    plt.xlabel("Время", fontsize=15, color="black")
    plt.ylabel("Входные переменные модели", fontsize=15, color="black")
    fig.tight_layout()
    fig.savefig('funcs.png')

    return plt.show()


root = Tk()
root.title("lab2")
root.geometry("600x800")

m0v = StringVar()
m1v = StringVar()
m2v = StringVar()
m3v = StringVar()
m4v = StringVar()
m5v = StringVar()
m6v = StringVar()
m7v = StringVar()
m8v = StringVar()
m9v = StringVar()

info = Label(text="Начальные значения: ")
m0 = Label(text="Угроза формирования «разделенной Америки»:")
m1 = Label(text="Затяжная пандемия коронавируса:")
m2 = Label(text="Соперничество стран в борьбе против изменения климата:")
m3 = Label(text="Усиление напряженности между США и Китаем:")
m4 = Label(text="Проблемы с передачей интернет-данных и их конфиденциальностью:")
m5 = Label(text="Конфликт в цифровом пространстве:")
m6 = Label(text="Политика президента Турции Реджепа Тайипа Эрдогана:")
m7 = Label(text="Падение экономики Ближнего Востока из-за снижения цен на нефть:")
m8 = Label(text="Уход Ангелы Меркель с поста канцлера Германии:")
m9 = Label(text="Политические и социальные проблемы в Латинской Америке:")
m10 = Label(text="Недостаточная эффективность вакцин из-за возникновения штаммов вируса с повышенной вирулентностью:")
m11 = Label(text="Недостаточная эффективность вакцин из-за возникновения штаммов вируса с повышенной летальностью:")
m12 = Label(text="Неспособность мировых элит к взаимным уступкам с целью скоординированной борьбы с пандемией:")
m13 = Label(text="Противостояние мировых центров силы:")
m14 = Label(text="Стремление мировых элит значительно усилить свое влияние в процессе борьбы с пандемией:")
m15 = Label(text="Недостаточная эффективность национальных систем здравоохранения в условиях пандемии:")


f1 = Label(text="F")
f2 = Label(text="F")
f3 = Label(text="F")
f4 = Label(text="F")
f5 = Label(text="F")

spin1 = Spinbox(from_=0, to=60, width=3)
spin1.grid(row=0, column=3)
spin2 = Spinbox(from_=0, to=60, width=3)
spin2.grid(row=1, column=3)
spin3 = Spinbox(from_=0, to=60, width=3)
spin3.grid(row=2, column=3)
spin4 = Spinbox(from_=0, to=60, width=3)
spin4.grid(row=3, column=3)
spin5 = Spinbox(from_=0, to=60, width=3)
spin5.grid(row=4, column=3)

x13 = Label(text="x^3 +")
x23 = Label(text="x^3 +")
x33 = Label(text="x^3 +")
x43 = Label(text="x^3 +")
x53 = Label(text="x^3 +")
x12 = Label(text="*x^2 +")
x11 = Label(text="*x +")
x22 = Label(text="*x^2 +")
x21 = Label(text="*x +")
x32 = Label(text="*x^2 +")
x31 = Label(text="*x +")
x42 = Label(text="*x^2 +")
x41 = Label(text="*x +")
x52 = Label(text="*x^2 +")
x51 = Label(text="*x +")

x13.grid(row=0, column=5, sticky="w")
x23.grid(row=1, column=5, sticky="w")
x33.grid(row=2, column=5, sticky="w")
x43.grid(row=3, column=5, sticky="w")
x53.grid(row=4, column=5, sticky="w")
x11.grid(row=0, column=9, sticky="w")
x12.grid(row=0, column=7, sticky="w")
x21.grid(row=1, column=9, sticky="w")
x22.grid(row=1, column=7, sticky="w")
x31.grid(row=2, column=9, sticky="w")
x32.grid(row=2, column=7, sticky="w")
x41.grid(row=3, column=9, sticky="w")
x42.grid(row=3, column=7, sticky="w")
x51.grid(row=4, column=9, sticky="w")
x52.grid(row=4, column=7, sticky="w")

info.grid(row=0, column=0, sticky="w")
m0.grid(row=1, column=0, sticky="w")
m1.grid(row=2, column=0, sticky="w")
m2.grid(row=3, column=0, sticky="w")
m3.grid(row=4, column=0, sticky="w")
m4.grid(row=5, column=0, sticky="w")
m5.grid(row=6, column=0, sticky="w")
m6.grid(row=7, column=0, sticky="w")
m7.grid(row=8, column=0, sticky="w")
m8.grid(row=9, column=0, sticky="w")
m9.grid(row=10, column=0, sticky="w")

f1.grid(row=0, column=2)
f2.grid(row=1, column=2)
f3.grid(row=2, column=2)
f4.grid(row=3, column=2)
f5.grid(row=4, column=2)

m0 = Entry(textvariable=m0v, width=3)
m1 = Entry(textvariable=m1v, width=3)
m2 = Entry(textvariable=m2v, width=3)
m3 = Entry(textvariable=m3v, width=3)
m4 = Entry(textvariable=m4v, width=3)
m5 = Entry(textvariable=m5v, width=3)
m6 = Entry(textvariable=m6v, width=3)
m7 = Entry(textvariable=m7v, width=3)
m8 = Entry(textvariable=m8v, width=3)
m9 = Entry(textvariable=m9v, width=3)

a00v = StringVar()
a01v = StringVar()
a02v = StringVar()
a03v = StringVar()
a04v = StringVar()
a05v = StringVar()

a10v = StringVar()
a11v = StringVar()
a12v = StringVar()
a13v = StringVar()
a14v = StringVar()
a15v = StringVar()

a20v = StringVar()
a21v = StringVar()
a22v = StringVar()
a23v = StringVar()
a24v = StringVar()
a25v = StringVar()

a00 = Entry(textvariable=a00v, width=3)
a01 = Entry(textvariable=a01v, width=3)
a02 = Entry(textvariable=a02v, width=3)
a03 = Entry(textvariable=a03v, width=3)
a04 = Entry(textvariable=a04v, width=3)

a10 = Entry(textvariable=a10v, width=3)
a11 = Entry(textvariable=a11v, width=3)
a12 = Entry(textvariable=a12v, width=3)
a13 = Entry(textvariable=a13v, width=3)
a14 = Entry(textvariable=a14v, width=3)

a20 = Entry(textvariable=a20v, width=3)
a21 = Entry(textvariable=a21v, width=3)
a22 = Entry(textvariable=a22v, width=3)
a23 = Entry(textvariable=a23v, width=3)
a24 = Entry(textvariable=a24v, width=3)

a30 = Entry(textvariable=a20v, width=3)
a31 = Entry(textvariable=a21v, width=3)
a32 = Entry(textvariable=a22v, width=3)
a33 = Entry(textvariable=a23v, width=3)
a34 = Entry(textvariable=a24v, width=3)

m0.grid(row=1, column=1, padx=5, pady=5)
m1.grid(row=2, column=1, padx=2, pady=2)
m2.grid(row=3, column=1, padx=5, pady=5)
m3.grid(row=4, column=1, padx=2, pady=2)
m4.grid(row=5, column=1, padx=5, pady=5)
m5.grid(row=6, column=1, padx=2, pady=2)
m6.grid(row=7, column=1, padx=5, pady=5)
m7.grid(row=8, column=1, padx=2, pady=2)
m8.grid(row=9, column=1, padx=5, pady=5)
m9.grid(row=10, column=1, padx=2, pady=2)

a00.grid(row=0, column=4, padx=5, pady=5)
a01.grid(row=4, column=4, padx=5, pady=5)
a02.grid(row=1, column=4, padx=2, pady=2)
a03.grid(row=2, column=4, padx=5, pady=5)
a04.grid(row=3, column=4, padx=2, pady=2)

a10.grid(row=0, column=6, padx=5, pady=5)
a11.grid(row=4, column=6, padx=5, pady=5)
a12.grid(row=1, column=6, padx=2, pady=2)
a13.grid(row=2, column=6, padx=5, pady=5)
a14.grid(row=3, column=6, padx=2, pady=2)

a20.grid(row=0, column=8, padx=2, pady=5)
a21.grid(row=4, column=8, padx=5, pady=5)
a22.grid(row=1, column=8, padx=2, pady=2)
a23.grid(row=2, column=8, padx=5, pady=5)
a24.grid(row=3, column=8, padx=2, pady=2)

a30.grid(row=0, column=10, padx=5, pady=5)
a31.grid(row=4, column=10, padx=5, pady=5)
a32.grid(row=1, column=10, padx=2, pady=2)
a33.grid(row=2, column=10, padx=5, pady=5)
a34.grid(row=3, column=10, padx=2, pady=2)

diagTv = StringVar()
diagT = Entry(textvariable=diagTv, width=3)
diagT.grid(row=8, column=8, padx=2, pady=2)

message_button = Button(text="Выполнить", command=calculate)
message_button.grid(row=5, column=7, padx=5, pady=5, sticky="e")
fak_button = Button(text="Графики возмущений", command=get_faks_image)
fak_button.grid(row=6, column=7, padx=5, pady=5, sticky="e")
graf_button = Button(text="Графики", command=get_graphics)
graf_button.grid(row=7, column=7, padx=5, pady=5, sticky="e")
diag_button = Button(text="Диаграммы", command=get_diag)
diag_button.grid(row=8, column=7, padx=5, pady=5, sticky="e")

root.mainloop()
