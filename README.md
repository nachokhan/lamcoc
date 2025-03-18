# 🚀 LAMCOC - Lambda Code Creator

**LAMCOC (Lambda Code Creator)** is a powerful and flexible tool for packaging Python projects for AWS Lambda functions. It allows you to define which files should be included in your Lambda deployment using a simple YAML configuration.

✅ **Fully customizable packaging**  
✅ **Supports dependency and library inclusion**  
✅ **No need for AWS-specific tools**  
✅ **Works in any project without additional setup**  

---

## 📥 Installation

### **Option 1: Clone the Repository**
```bash
git clone https://github.com/nachokhan/lamcoc.git
cd lamcoc
```

### **Option 2: Create a Global Command**
If you want to run `lamcoc` from anywhere, create a symbolic link:

_(TIP: you might need to run this as root)_

```bash
ln -s "$(pwd)/lamcoc.py" /usr/local/bin/lamcoc
chmod +x /usr/local/bin/lamcoc
```
Now you can use `lamcoc` globally!

---

## 🚀 Usage

Run `lamcoc` in any project that contains a **`include.yaml`** file.

### **1️⃣ Generate a ZIP Plan**
Check which files will be included before creating the package:
```bash
lamcoc plan
```
This generates:
- **`plan_to_zip.txt`** → Shows files in their original locations (file to be included in the zip)
- **`planned_zip.txt`** → Shows files as they will appear inside the ZIP.

### **2️⃣ Create the Lambda Package**
Generate the final `lambda.zip` ready for deployment:
```bash
lamcoc create
```
This creates:
- **`lambda.zip`** → The final AWS Lambda package.

---

## 📝 Configuration (include.yaml)

Create a file named **`include.yaml`** in your project directory to specify files and dependencies.

### **Example `include.yaml`**
```yaml
include:
  - "*.py"       # Recursively include all Python files
  - "mock_data/**/*" # Include all files in mock_data/

exclude:
  - "avoid_this_folder/*.py" # Exclude files in this folder
  - "config/secrets.yaml"    # Exclude specific file
  - "**/*.log"               # Exclude log files
  - ".env/**/*.py"           # Exclude Python files inside .env/

libraries:
  - ".env/lib/python3.11/site-packages" # Include all pip-installed libs
```

---

## 📦 How Files Are Packaged

- **Regular files** retain their **original structure**.
- **Library files** are moved to the **root of the ZIP**, preserving internal structure.

### **Example**
#### **Project Structure**
```
my_project/
│── main.py
│── utils.py
│── mock_data/
│   ├── test.json
│── external_libs/
│   ├── my_lib.py
│   ├── utils/
│   │   ├── helper.py
│── include.yaml
```
#### **Final `planned_zip.txt`**
```
main.py
utils.py
mock_data/test.json
my_lib.py  # Moved to ZIP root
utils/helper.py  # Preserves subfolder from external_libs/
```
---

## 🚀  Upload to AWS LAMBDA

Now you can upload the file to your AWS Lambda!

---

## 🔥 Future Features
- `lamcoc deploy` → Deploy directly to AWS Lambda.
- `lamcoc test` → Run local tests before packaging.
- `--use-requirements` → Auto-install dependencies.

---

## 📄 License
MIT License. Contributions are welcome! 🎉

---

## 💡 Contributions
1. Fork the repo.
2. Make your improvements.
3. Submit a PR!
