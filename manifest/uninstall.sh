kubectl delete -f postgres-deployment.yaml 
kubectl delete -f postgres-service.yaml
kubectl delete -f streamlit-deployment.yaml 
kubectl delete -f streamlit-service.yaml 
kubectl delete -f ingress.yaml
kubectl delete ns coolstat
