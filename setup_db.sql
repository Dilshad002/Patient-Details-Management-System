USE hospital_management;

CREATE TABLE patients1 (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age INT NOT NULL,
    gender VARCHAR(10) NOT NULL,
    address VARCHAR(255) NOT NULL,
    admission_date DATE NOT NULL
);

CREATE TABLE lab_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    test_name VARCHAR(100) NOT NULL,
    result VARCHAR(255) NOT NULL,
    date DATE NOT NULL,
    FOREIGN KEY (patient_id) REFERENCES patients(id)
);

CREATE TABLE billing (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    date DATE NOT NULL,
    FOREIGN KEY (patient_id) REFERENCES patients(id)
);

SHOW CREATE TABLE billing;
ALTER TABLE billing DROP FOREIGN KEY billing_ibfk_1;
ALTER TABLE billing ADD CONSTRAINT billing_ibfk_1 FOREIGN KEY (patient_id) REFERENCES patients1(id);

SHOW CREATE TABLE lab_data;
ALTER TABLE lab_data DROP FOREIGN KEY lab_data_ibfk_1;
ALTER TABLE lab_data ADD CONSTRAINT lab_data_ibfk_1 FOREIGN KEY (patient_id) REFERENCES patients1(id);

ALTER TABLE patients1
ADD COLUMN checkup_details TEXT NULL,
ADD COLUMN prescriptions TEXT NULL;

-- Drop the existing foreign key constraint
ALTER TABLE lab_data DROP FOREIGN KEY lab_data_ibfk_1;
-- Add a new foreign key constraint with ON DELETE CASCADE
ALTER TABLE lab_data ADD CONSTRAINT lab_data_ibfk_1 FOREIGN KEY (patient_id) REFERENCES patients1(id) ON DELETE CASCADE;

ALTER TABLE billing DROP FOREIGN KEY billing_ibfk_1;
-- Add a new foreign key constraint with ON DELETE CASCADE
ALTER TABLE billing ADD CONSTRAINT billing_ibfk_1 FOREIGN KEY (patient_id) REFERENCES patients1(id) ON DELETE CASCADE;

