# **Weekly Cloud Build CI/CD Pipeline Documentation**

## **Introduction**
This documentation describes the Continuous Integration/Continuous Deployment (CI/CD) pipeline for deploying a **FastAPI** application using **Google Cloud Build**. The process involves building a Docker image, pushing it to Google Container Registry (GCR), and deploying it to **Google Cloud Run**.

---

## **Prerequisites**
Before getting started, ensure the following prerequisites are met:

1. **Google Cloud Platform (GCP) Account**:
   - You must have an active GCP account with access to a project.
   
2. **Cloud Build API**:
   - Enable the **Cloud Build API** in your GCP project.
   ```bash
   gcloud services enable cloudbuild.googleapis.com
   ```

3. **Docker**:
   - Docker must be installed locally to build and test the image.

---

## **Cloud Build Configuration**
The CI/CD pipeline is defined in the `cloudbuild.yaml` configuration file. This file automates the following steps: **Build**, **Push**, and **Deploy**.

### **1. Build Docker Image**
- The Docker image for the FastAPI application is built using the **docker build** command.
- The image is tagged for future use.

Sample configuration in `cloudbuild.yaml`:
```yaml
steps:
  - name: 'gcr.io/cloud-builders/docker'
    args:
      - 'build'
      - '-t'
      - 'gcr.io/$PROJECT_ID/fastapi-app:$SHORT_SHA'
      - '.'
```

### **2. Push to Google Container Registry (GCR)**
- The built image is pushed to **Google Container Registry (GCR)** for centralized storage and management.

Configuration for the push step:
```yaml
  - name: 'gcr.io/cloud-builders/docker'
    args:
      - 'push'
      - 'gcr.io/$PROJECT_ID/fastapi-app:$SHORT_SHA'
```

### **3. Deploy to Google Cloud Run**
- The application is deployed to **Google Cloud Run** using the **gcloud run deploy** command.
- The image from GCR and the region are specified.

Deployment configuration:
```yaml
  - name: 'gcr.io/cloud-builders/gcloud'
    args:
      - 'run'
      - 'deploy'
      - 'fastapi-service'
      - '--image=gcr.io/$PROJECT_ID/fastapi-app:$SHORT_SHA'
      - '--region=us-central1'
      - '--platform=managed'
```

### **Full `cloudbuild.yaml` File**
Here is the complete `cloudbuild.yaml` configuration:
```yaml
steps:
  - name: 'gcr.io/cloud-builders/docker'
    args:
      - 'build'
      - '-t'
      - 'gcr.io/$PROJECT_ID/fastapi-app:$SHORT_SHA'
      - '.'

  - name: 'gcr.io/cloud-builders/docker'
    args:
      - 'push'
      - 'gcr.io/$PROJECT_ID/fastapi-app:$SHORT_SHA'

  - name: 'gcr.io/cloud-builders/gcloud'
    args:
      - 'run'
      - 'deploy'
      - 'fastapi-service'
      - '--image=gcr.io/$PROJECT_ID/fastapi-app:$SHORT_SHA'
      - '--region=us-central1'
      - '--platform=managed'

images:
  - 'gcr.io/$PROJECT_ID/fastapi-app:$SHORT_SHA'
```

---

## **How to Trigger the Pipeline**
trigger the pipeline via the Google Cloud Console or by running the following command:
```bash
gcloud builds submit --config cloudbuild.yaml .
```

---

## **Conclusion**
This CI/CD pipeline automates the following steps:
1. **Build**: Creates a Docker image of the FastAPI application.
2. **Push**: Uploads the image to **Google Container Registry (GCR)**.
3. **Deploy**: Deploys the application to **Google Cloud Run**.

