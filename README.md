# TestOps Insider – Selenium Kubernetes Projesi

Bu projede Selenium testlerini Docker ve Kubernetes kullanarak çalıştırdım.  
Amaç, testlerin tarayıcıdan bağımsız, ölçeklenebilir ve AWS üzerinde çalışabilir hale getirilmesidir.

Proje hem lokal Kubernetes ortamında hem de AWS EKS üzerinde çalışacak şekilde hazırlanmıştır.

---

## Genel Sistem Özeti

Sistem iki ana parçadan oluşur:

- Testleri çalıştıran bir Test Controller
- Testlerin çalıştığı Chrome Node’lar

Test Controller test senaryolarını alır ve Selenium üzerinden Chrome Node’lara gönderir.  
Chrome Node’lar ise headless Chrome tarayıcı üzerinde testleri çalıştırır.

---

## Mimari Yapı

### Test Controller Pod

- Python ve pytest kullanır
- Selenium testlerini çalıştırır
- Remote WebDriver ile Chrome Node’a bağlanır
- Kubernetes Job olarak çalışır (iş bitince kapanacak şekilde ayarlandı)

### Chrome Node Pod

- Headless Chrome tarayıcı çalıştırır
- Selenium standalone Chrome image kullanır
- Birden fazla pod olarak çalışabilir

---

## Pod’lar Arası İletişim

Pod’lar bir Kubernetes Service üzerinden haberleşir.

- Service adı: `chrome-service`
- Selenium endpoint:

http://chrome-service:4444

Test Controller bu adresi kullanarak Chrome Node’lara bağlanır.  
DNS çözümlemesi Kubernetes tarafından otomatik yapılır.

---

## Docker Yapısı

### Test Controller Docker Image

- Python
- Selenium
- pytest
- Test dosyaları

içerir ve Docker Hub’a push edilmiştir.

### Chrome Node Docker Image

- Selenium’un hazır standalone Chrome image’ı kullanılmıştır
- Headless Chrome çalışır

---

## Kubernetes Kaynakları

Projede aşağıdaki Kubernetes kaynakları kullanılmıştır:

- Deployment: Chrome Node’lar için
- Service: Chrome Node’lara erişim için
- Job: Test Controller için
- HPA: Chrome Node’ların otomatik ölçeklenmesi için
(ilgili path üzeerinde belirtilmiştir)

HPA ayarları:
- Minimum pod: 1
- Maksimum pod: 5

Tüm YAML dosyaları `k8s/` klasörü altındadır.

---

## Python Deploy Script

`scripts/deploy.py` dosyası Kubernetes sürecini otomatikleştirir.

Bu script şunları yapar:

- Chrome Node sayısını ayarlar
- Pod’ların hazır olmasını bekler
- Eski test job’unu siler
- Yeni test job’unu oluşturur
- Test pod’u hazır olana kadar bekler
- Test loglarını ekrana basar

Bu sayede manuel kubectl komutları yazmaya gerek kalmaz.

---

## Lokal Kubernetes Üzerinde Çalıştırma

```bash
kubectl apply -f k8s/
kubectl get pods
kubectl logs job/test-controller

-veya AWS EKS üzerinde otomatik olarak

 -AWS üzerinde EKS cluster oluşturulur
 -Node group eklenir
 -kubectl erişimi ayarlanır
 -Kubernetes dosyaları deploy edilir
 -Testler çalıştırılır
 
aws eks update-kubeconfig --region <region> --name <cluster-name>
kubectl apply -f k8s/
python3 scripts/deploy.py

<img width="1043" height="255" alt="error" src="https://github.com/user-attachments/assets/7c7f7e74-2585-4a75-a65a-465d92ffa1bf" />
<img width="1256" height="221" alt="error1" src="https://github.com/user-attachments/assets/d9739a81-a924-40df-8233-dfafec75a287" />
<img width="1198" height="178" alt="solved" src="https://github.com/user-attachments/assets/0d8030c1-d0d9-4c3e-b409-791460e6161f" />

<img width="1895" height="761" alt="eks-node-group" src="https://github.com/user-attachments/assets/ffe87044-099b-4d5f-bc33-625b7f832198" />
<img width="880" height="172" alt="test-logs-result" src="https://github.com/user-attachments/assets/e8683459-4bbf-4e63-b4c6-f397ce70bed6" />
<img width="1056" height="273" alt="test-logs" src="https://github.com/user-attachments/assets/be4288fa-9c92-4dc4-ba98-a46dc614329a" />
<img width="762" height="80" alt="eks-pods" src="https://github.com/user-attachments/assets/89b08231-8c2c-4112-9d55-40456d53e040" />
<img width="679" height="72" alt="eks-nodes" src="https://github.com/user-attachments/assets/2dbe4d9d-f038-4795-8cf9-b982d4da794b" />

