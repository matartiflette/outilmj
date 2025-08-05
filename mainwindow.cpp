#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QFile>
#include <QTextStream>
#include <QCloseEvent>

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent), ui(new Ui::MainWindow) {
    ui->setupUi(this);
    chargerFichiers();
}

MainWindow::~MainWindow() {
    delete ui;
}

void MainWindow::chargerFichiers() {
    QFile stats("stats.txt");
    if (stats.open(QIODevice::ReadOnly | QIODevice::Text))
        ui->textStats->setPlainText(QTextStream(&stats).readAll());

    QFile stuff("stuffs.txt");
    if (stuff.open(QIODevice::ReadOnly | QIODevice::Text))
        ui->textStuff->setPlainText(QTextStream(&stuff).readAll());

    QFile hist("histoire.txt");
    if (hist.open(QIODevice::ReadOnly | QIODevice::Text))
        ui->textHistoire->setPlainText(QTextStream(&hist).readAll());
}

void MainWindow::sauvegarderFichiers() {
    QFile stats("stats.txt");
    if (stats.open(QIODevice::WriteOnly | QIODevice::Text))
        QTextStream(&stats) << ui->textStats->toPlainText();

    QFile stuff("stuffs.txt");
    if (stuff.open(QIODevice::WriteOnly | QIODevice::Text))
        QTextStream(&stuff) << ui->textStuff->toPlainText();

    QFile hist("histoire.txt");
    if (hist.open(QIODevice::WriteOnly | QIODevice::Text))
        QTextStream(&hist) << ui->textHistoire->toPlainText();
}

void MainWindow::closeEvent(QCloseEvent *event) {
    sauvegarderFichiers();
    event->accept();
}
