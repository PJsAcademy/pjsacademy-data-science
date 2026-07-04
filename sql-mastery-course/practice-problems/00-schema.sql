-- ============================================================
-- PJ's Academy — SQL Practice Bank · Shared Schema
-- Run this once to create the sample tables used by all 100 problems.
-- Works in standard SQL (MySQL/Postgres) and Snowflake.
-- ============================================================

-- ---------- Departments ----------
CREATE TABLE departments (
    dept_id    INT PRIMARY KEY,
    dept_name  VARCHAR(50),
    location   VARCHAR(50)
);

-- ---------- Employees ----------
CREATE TABLE employees (
    emp_id      INT PRIMARY KEY,
    name        VARCHAR(50),
    dept_id     INT,             -- FK -> departments.dept_id
    manager_id  INT,             -- self FK -> employees.emp_id (NULL for CEO)
    salary      INT,
    hire_date   DATE,
    email       VARCHAR(100)
);

-- ---------- Customers ----------
CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    name        VARCHAR(50),
    city        VARCHAR(50),
    signup_date DATE
);

-- ---------- Products ----------
CREATE TABLE products (
    product_id  INT PRIMARY KEY,
    product_name VARCHAR(50),
    category    VARCHAR(50),
    price       DECIMAL(10,2)
);

-- ---------- Orders ----------
CREATE TABLE orders (
    order_id    INT PRIMARY KEY,
    customer_id INT,             -- FK -> customers.customer_id
    product_id  INT,             -- FK -> products.product_id
    quantity    INT,
    order_date  DATE,
    amount      DECIMAL(10,2)
);

-- ---------- Sample data ----------
INSERT INTO departments VALUES
 (1,'Engineering','Bangalore'),(2,'Sales','Mumbai'),
 (3,'Marketing','Delhi'),(4,'HR','Bangalore');

INSERT INTO employees VALUES
 (1,'Asha',1,NULL,180000,'2019-03-01','asha@pjs.com'),
 (2,'Ravi',1,1,120000,'2020-06-15','ravi@pjs.com'),
 (3,'Meera',2,1,95000,'2021-01-20','meera@pjs.com'),
 (4,'Kiran',2,3,70000,'2022-07-11','kiran@pjs.com'),
 (5,'Sana',3,1,88000,'2021-09-05','sana@pjs.com'),
 (6,'Vijay',1,2,110000,'2023-02-28','vijay@pjs.com'),
 (7,'Nina',4,1,60000,'2020-11-30',NULL);

INSERT INTO customers VALUES
 (101,'Rahul','Mumbai','2023-01-10'),
 (102,'Priya','Delhi','2023-02-14'),
 (103,'Arjun','Bangalore','2023-03-22'),
 (104,'Divya','Mumbai','2023-05-01');

INSERT INTO products VALUES
 (201,'Laptop','Electronics',55000.00),
 (202,'Mouse','Electronics',700.00),
 (203,'Desk','Furniture',8000.00),
 (204,'Chair','Furniture',4500.00),
 (205,'Monitor','Electronics',15000.00);

INSERT INTO orders VALUES
 (1,101,201,1,'2023-06-01',55000.00),
 (2,101,202,2,'2023-06-01',1400.00),
 (3,102,205,2,'2023-06-05',30000.00),
 (4,103,203,1,'2023-06-10',8000.00),
 (5,103,204,4,'2023-06-10',18000.00),
 (6,104,201,1,'2023-07-02',55000.00),
 (7,102,202,1,'2023-07-15',700.00),
 (8,101,205,1,'2023-08-01',15000.00);
