import subprocess
import time


def run(cmd):
    print(f"> {cmd}")
    return subprocess.run(
        cmd,
        shell=True,
        check=False,
        capture_output=True,
        text=True
    )


print(" Chrome node scale ediliyor...")
run("kubectl scale deployment chrome --replicas=1")

print(" Chrome pod'larının hazır olması bekleniyor...")
run("kubectl wait --for=condition=available deployment/chrome --timeout=120s")

print(" Eski test job siliniyor (varsa)...")
run("kubectl delete job test-controller --ignore-not-found")

print(" Test job oluşturuluyor...")
run("kubectl apply -f k8s/controller-job.yaml")

print(" Test pod'unun başlaması bekleniyor...")
time.sleep(10)

print("⏳ Test pod'u Ready olana kadar bekleniyor...")
run(
    "kubectl wait "
    "--for=condition=ready pod "
    "-l job-name=test-controller "
    "--timeout=120s"
)

print(" Test logları:")
logs = run("kubectl logs job/test-controller")
print(logs.stdout)

print(" Script tamamlandı.")

