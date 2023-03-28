import sys
from typing import Union, Any

import pandas as pd
from pandas import DataFrame
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.svm import SVC
from scapy.all import *
from datetime import datetime
import sqlite3

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog, QMessageBox
from PyQt5.uic import loadUi


# Load NSL-KDD dataset
df: Union[DataFrame, Any] = pd.read_csv('KDDTest+.txt')

# Preprocessing
df['class'] = (df['class']
               .replace(['back', 'land', 'neptune', 'pod', 'smurf', 'teardrop', 'apache2', 'udpstorm', 'processtable', 'worm'], 'attack')
               .replace(['ipsweep', 'nmap', 'portsweep', 'satan'], 'probe')
               .replace(['buffer_overflow', 'loadmodule', 'perl', 'rootkit'], 'u2r')
               .replace(['ftp_write', 'guess_passwd', 'imap', 'multihop', 'phf', 'spy', 'warezclient', 'warezmaster'], 'r2l'))


# Create feature and target arrays
X = df.iloc[:, :-2].values
y = df.iloc[:, -2].values

# Scale feature values
scaler = StandardScaler()
X = scaler.fit_transform(X)

# Train SVM model
clf = SVC(kernel='rbf', C=1, gamma='auto')
clf.fit(X, y)


# Define function to extract packet features
def extract_features(packet):
    features = []

    # IP source and destination addresses
    src = packet[IP].src
    dst = packet[IP].dst
    features.append(src)
    features.append(dst)

    # Protocol
    protocol = packet[IP].proto
    features.append(protocol)

    # Service
    if TCP in packet:
        service = packet[TCP].dport
    elif UDP in packet:
        service = packet[UDP].dport
    else:
        service = 0
    features.append(service)

    # Flag
    if TCP in packet:
        flag = packet[TCP].flags
    else:
        flag = ''
    features.append(flag)

    # Packet length
    length = len(packet)
    features.append(length)

    return features


# Log kaydı yapmak için veritabanı bağlantısı aç
conn = sqlite3.connect('log_database.db')
c = conn.cursor()

# Log tablosunu oluştur
c.execute('''CREATE TABLE IF NOT EXISTS log_table
             (date_time text, attack_type text)''')


# Saldırı tespit edildiğinde log kaydı yap
def log_attack(attack_type):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO log_table VALUES (?,?)", (current_time, attack_type))
    conn.commit()


# Veritabanı bağlantısını kapat
def close_db():
    conn.close()


# Define function to classify packets in real-time and log attacks
def classify_packets(packet):
    features = extract_features(packet)
    X = scaler.transform([features])
    y_pred = clf.predict(X)
    if y_pred == 1:
        attack_type = 'unknown'
        if packet[IP].src == '192.168.0.10':
            attack_type = 'internal'
        elif packet[IP].src == '192.168.0.100':
            attack_type = 'external'
        log_attack(attack_type)
        print(f"Anomaly detected: {packet[IP].src} -> {packet[IP].dst}, Attack type: {attack_type}")


class PacketClassifierUI(QDialog):
    def __init__(self):
        super(PacketClassifierUI, self).__init__()
        loadUi('packet_classifier.ui', self)

        self.browseButton.clicked.connect(self.browse_file)
        self.startButton.clicked.connect(self.start_classification)

    def browse_file(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', 'c:\\', "PCAP files (*.pcap)")
        self.filePath.setText(fname[0])

    def start_classification(self):
        file_path = self.filePath.text()
        if file_path == '':
            QMessageBox.critical(self, "Error", "Please select a PCAP file to classify")
            return

        # Load PCAP file and classify packets
        packets = rdpcap(file_path)
        for packet in packets:
            try:
                classify_packets(packet)
            except Exception as e:
                print(f"Error classifying packet: {e}")
        close_db()
        QMessageBox.information(self, "Success", "Classification complete and log saved to database")


class PacketClassifier:
    pass