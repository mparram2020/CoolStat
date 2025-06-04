kubectl create ns coolstat
kubectl apply -f postgres-deployment.yaml 
kubectl apply -f postgres-service.yaml
kubectl apply -f streamlit-deployment.yaml 
kubectl apply -f streamlit-service.yaml 
kubectl apply -f ingress.yaml
