IF OBJECT_ID('websites_data', 'U') IS NOT NULL
    DROP TABLE websites_data;

-- Create the websites_data table
CREATE TABLE websites_data 
(
    id INT IDENTITY(1,1) PRIMARY KEY,
    domain_name NVARCHAR(MAX),
    date_loaded DATETIME DEFAULT GETDATE(),
    date_processed DATETIME NULL,
    process_status VARCHAR(50) NULL CHECK (process_status IN ('Inprogress', 'Completed', 'Failed')),
    is_qualified NVARCHAR(3) NULL CHECK (is_qualified IN ('Yes', 'No')),
    total_links INT,
    last_log_stats NVARCHAR(MAX)
);

SELECT * FROM websites_data

insert into websites_data(domain_name)
values
('cbbtraffic.com'),
('premiercivil.com'),
('gonzalezcos.com'),
('ctcbear.com'),
('atlantictesting.com'),
('khhpc.com'),
('cscos.com'),
('bartonandloguidice.com'),
('cmeassociates.com'),
('ryanbiggs.com'),
('asm4.com'),
('infrastructure-eng.com'),
('firstgroupengineering.com'),
('cbbel-in.com'),
('structurepoint.com'),
('ucindy.com'),
('eticagroup.com'),
('beamsuntory.com'),
('usiconsultants.com'),
('sjcainc.com'),
('aapprecisionplanning.com'),
('vsengineering.com')