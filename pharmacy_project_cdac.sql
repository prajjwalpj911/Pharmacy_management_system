create database pharmacy;

use pharmacy;

CREATE TABLE IF NOT EXISTS medicines (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        quantity INT,
        price DECIMAL(10, 2));
        
select * from medicines;

delete from medicines where name = 'bicasules';
