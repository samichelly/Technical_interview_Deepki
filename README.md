# Technical Interview Deepki

## **Objective**  
The goal of this project is to download, process, and analyze building footprint data from a public dataset. The output includes processed data visualizations saved as HTML files, which can be viewed in a browser. This repository provides two methods for running the workflow: using Google Colab or Docker.

---

## **Requirements**  
- For Google Colab: A Google account.  
- For Docker: A local installation of Docker.  

---

## **Usage Instructions**  

### **Method 1: Using Google Colab**  
1. Open the provided [Google Colab Notebook] [here](https://colab.research.google.com/drive/1zE1BYE-AlZaNv8d2qcP4M32_DJU52w2H?usp=sharing).
2. Run the notebook

### **Method 2: Using Docker**  
1. Clone this repository:  
    ```bash
    https://github.com/samichelly/Technical_interview_Deepki.git
    cd Technical_interview_Deepki
    ```  

2. Build the Docker image:  
    ```bash
    docker build -t Technical_interview_Deepki .
    ```  

3. Run the container:  
    ```bash
    docker run -it Technical_interview_Deepki
    ```  

4. Once the processing is complete, the closest building will be display in the terminal  
  
