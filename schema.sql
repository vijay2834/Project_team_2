DROP TABLE IF EXISTS ORDERPET;
DROP TABLE IF EXISTS ORDERPRODUCT;
DROP TABLE IF EXISTS `ORDER`;
DROP TABLE IF EXISTS PAYMENT;
DROP TABLE IF EXISTS ADDRESS;
DROP TABLE IF EXISTS USER;
DROP TABLE IF EXISTS PRODUCT;
DROP TABLE IF EXISTS PET;
DROP TABLE IF EXISTS CATEGORY;
DROP TABLE IF EXISTS BREED;
DROP TABLE IF EXISTS ROLE;

# Create ROLE table
CREATE TABLE IF NOT EXISTS ROLE (
    RoleID INT AUTO_INCREMENT PRIMARY KEY,
    RoleName VARCHAR(50)
);

# Create USER table
CREATE TABLE IF NOT EXISTS USER (
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    RoleID INT,
    FirstName VARCHAR(70),
    LastName VARCHAR(70),
    Email VARCHAR(100),
    Phone VARCHAR(20),
    Password VARCHAR(255),
    CreatedDateTime DATETIME,
    FOREIGN KEY (RoleID) REFERENCES ROLE(RoleID)
);

# Create ADDRESS table
CREATE TABLE IF NOT EXISTS ADDRESS (
    AddressID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT,
    Street1 VARCHAR(100),
    Street2 VARCHAR(100),
    City VARCHAR(50),
    State VARCHAR(50),
    Zip VARCHAR(20),
    CurrentYesOrNo BOOLEAN,
    FOREIGN KEY (UserID) REFERENCES USER(UserID)
);

# Create TRANSACTION table
CREATE TABLE IF NOT EXISTS PAYMENT (
    PaymentID INT AUTO_INCREMENT PRIMARY KEY,
    PaymentMethod VARCHAR(50),
    Amount DECIMAL(10,2),
    Date DATETIME,
    Status VARCHAR(20)
);

# Create ORDER table
CREATE TABLE IF NOT EXISTS `ORDER` (
    OrderID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT,
    PaymentID INT,
    OrderedDate DATETIME,
    TotalAmount DECIMAL(10,2),
    OrderStatus VARCHAR(20),
    DeliveryStatus VARCHAR(20),
    DeliveryDate DATETIME,
    FOREIGN KEY (UserID) REFERENCES USER(UserID),
    FOREIGN KEY (PaymentID) REFERENCES PAYMENT(PaymentID)
);

# Create CATEGORY table
CREATE TABLE IF NOT EXISTS CATEGORY (
    CategoryID INT AUTO_INCREMENT PRIMARY KEY,
    CategoryName VARCHAR(100)
);

# Create PRODUCT table
CREATE TABLE IF NOT EXISTS PRODUCT (
    ProductID INT AUTO_INCREMENT PRIMARY KEY,
    CategoryID INT,
    ProductName VARCHAR(100),
    Description TEXT,
    Price DECIMAL(10,2),
    Stock INT,
    FOREIGN KEY (CategoryID) REFERENCES CATEGORY(CategoryID)
);

# Create BREED table
CREATE TABLE IF NOT EXISTS BREED (
    BreedID INT AUTO_INCREMENT PRIMARY KEY,
    BreedName VARCHAR(100)
);

# Create PET table
CREATE TABLE IF NOT EXISTS PET (
    PetID INT AUTO_INCREMENT PRIMARY KEY,
    BreedID INT,
    PetName VARCHAR(100),
    Age INT,
    Price DECIMAL(10,2),
    FOREIGN KEY (BreedID) REFERENCES BREED(BreedID)
);

# Create ORDERPRODUCT table
CREATE TABLE IF NOT EXISTS ORDERPRODUCT (
    OrderProductID INT AUTO_INCREMENT PRIMARY KEY,
    OrderID INT,
    ProductID INT,
    Quantity INT,
    TotalItemAmount DECIMAL(10,2),
    FOREIGN KEY (OrderID) REFERENCES `ORDER`(OrderID),
    FOREIGN KEY (ProductID) REFERENCES PRODUCT(ProductID)
);

# Create ORDERPET table
CREATE TABLE IF NOT EXISTS ORDERPET (
    OrderPetID INT AUTO_INCREMENT PRIMARY KEY,
    OrderID INT,
    PetID INT,
    Quantity INT,
    TotalItemAmount DECIMAL(10,2),
    FOREIGN KEY (OrderID) REFERENCES `ORDER`(OrderID),
    FOREIGN KEY (PetID) REFERENCES PET(PetID)
);

INSERT INTO ROLE (RoleName) 
VALUES 
    ('ADMIN'),
    ('CUSTOMER');

INSERT INTO USER (RoleID, FirstName, LastName, Email, Phone, Password, CreatedDateTime) 
VALUES
(2, 'Jordain', 'MacCook', 'jmaccook0@histats.com', '(487) 8683346', 'dX8+UWZa(mdo', '2022-10-13 20:55:48'),
(1, 'Giffer', 'Filpi', 'gfilpi1@slashdot.org', '(944) 4312428', 'oD1#qrLc(@', '2020-07-28 04:47:47'),
(1, 'Penny', 'Lennie', 'plennie2@google.it', '(850) 3531886', 'mV7>em!3bdUPc', '2024-02-24 06:30:35'),
(2, 'Wrennie', 'Scouller', 'wscouller3@java.com', '(575) 1395007', 'hU8?1&s5sHG!', '2019-11-22 01:18:12'),
(1, 'Adeline', 'Morman', 'amorman4@shinystat.com', '(846) 1697216', 'iY7_HA''yk', '2023-01-05 16:38:04'),
(2, 'Huntlee', 'Slowgrave', 'hslowgrave5@digg.com', '(170) 1052515', 'cT2/dGw"I8m*', '2022-01-15 19:02:56'),
(1, 'Annabella', 'Harlowe', 'aharlowe6@tmall.com', '(453) 2159626', 'uS0,,{nByW|qhdcq', '2024-05-02 19:21:52'),
(1, 'Agnese', 'Ivanets', 'aivanets7@bloglovin.com', '(124) 1576406', 'oJ4.n&&Tv6&', '2023-12-17 05:06:53'),
(2, 'Wilton', 'Kitchenman', 'wkitchenman8@bbc.co.uk', '(114) 1161295', 'vQ2*1&#\NnD=x#W', '2021-05-24 22:19:07'),
(2, 'Hayley', 'Ber', 'hber9@ted.com', '(592) 7196078', 'tM2?##Tjy\|`d', '2023-12-20 20:55:03'),
(1, 'Tore', 'Malyj', 'tmalyja@symantec.com', '(702) 4400417', 'dO9)y6Y7R><', '2024-02-17 02:00:25'),
(2, 'Rickey', 'Chapiro', 'rchapirob@soundcloud.com', '(643) 6586662', 'tX7\2&/\,A!=Zm', '2021-03-04 20:04:45'),
(2, 'Erasmus', 'Manuello', 'emanuelloc@google.cn', '(913) 2940065', 'wA7$u%mBp1Hc"', '2022-12-20 09:36:28'),
(2, 'Merrie', 'Dory', 'mdoryd@mayoclinic.com', '(270) 8530499', 'dR9<vFJe4<', '2021-06-25 22:42:38'),
(1, 'Philbert', 'Gladdolph', 'pgladdolphe@wikia.com', '(194) 7712555', 'uC7&,f=HlNu0n', '2023-06-19 05:26:17'),
(2, 'Ardys', 'Thornham', 'athornhamf@flavors.me', '(460) 9728738', 'pL1?nU.hV<?C', '2021-03-26 07:49:12'),
(2, 'Anatola', 'Gallimore', 'agallimoreg@twitpic.com', '(685) 5068776', 'zI8%_+`}dE)?og', '2023-06-06 20:22:02'),
(1, 'Ricki', 'Bernollet', 'rbernolleth@globo.com', '(441) 9993773', 'aW6|W''''COlh&', '2019-09-22 22:51:33'),
(2, 'Karlan', 'Marien', 'kmarieni@eventbrite.com', '(925) 4859080', 'lG3#IW(Fwu70iw,', '2023-08-22 05:03:40'),
(1, 'Ann', 'Wilcot', 'awilcotj@over-blog.com', '(494) 6413193', 'cU6%EuX\2$W?m0(', '2020-11-10 04:48:22'),
(1, 'Lorena', 'Frow', 'lfrowk@amazon.co.jp', '(599) 7264564', 'pN3&M>t)QD<!7"+', '2023-03-20 04:05:26'),
(1, 'Ricard', 'Moyler', 'rmoylerl@yellowbook.com', '(364) 3418725', 'vO8!P?ipgn', '2019-05-22 09:23:46'),
(1, 'Gerianne', 'Tames', 'gtamesm@pinterest.com', '(336) 8681266', 'gH3{''>w*?#M', '2024-02-26 05:07:51'),
(1, 'Fawne', 'Moxom', 'fmoxomn@pagesperso-orange.fr', '(609) 7314534', 'mX6}J@e<Zf#0', '2022-06-18 23:30:43'),
(2, 'Loleta', 'Mynett', 'lmynetto@amazon.co.uk', '(854) 9086052', 'vO0)qV7,yn''XxYy', '2024-12-22 19:02:31'),
(1, 'Ekaterina', 'Deverell', 'edeverellp@psu.edu', '(189) 4809834', 'bM3@Xxe`=jD''', '2021-04-14 02:24:48'),
(2, 'Aretha', 'Blacklock', 'ablacklockq@un.org', '(472) 3798041', 'vN1~yPj{nb!', '2021-04-08 06:23:37'),
(2, 'Appolonia', 'Swindells', 'aswindellsr@mysql.com', '(453) 1677187', 'wT9&bo''@t`W\Wf4', '2019-06-19 17:01:37'),
(2, 'Cherye', 'Cheers', 'ccheerss@cbc.ca', '(626) 6075966', 'cM2@sC@{?YT,', '2020-01-08 17:09:44'),
(2, 'Letisha', 'Purkess', 'lpurkesst@accuweather.com', '(712) 3087479', 'xV6.1Qai/,oCJ', '2024-02-11 07:15:21');

INSERT INTO ADDRESS (UserID, Street1, Street2, City, State, Zip, CurrentYesOrNo) 
VALUES
(21, '071 Hanover Center', 'APT M4', 'Springfield', 'Missouri', '65805', TRUE),
(2, '54688 Gulseth Parkway', 'APT N3', 'Santa Fe', 'New Mexico', '87592', FALSE),
(20, '80 Laurel Trail', 'APT M2', 'Stockton', 'California', '95210', FALSE),
(18, '9732 Cottonwood Place', 'APT K8', 'Fort Worth', 'Texas', '76121', FALSE),
(27, '6915 Cordelia Terrace', 'APT D3', 'Reading', 'Pennsylvania', '19610', FALSE),
(19, '74766 Dixon Lane', 'APT H5', 'Saint Petersburg', 'Florida', '33742', TRUE),
(4, '0143 Canary Lane', 'APT S6', 'Baton Rouge', 'Louisiana', '70810', FALSE),
(20, '516 Lake View Terrace', 'APT N8', 'Sioux Falls', 'South Dakota', '57110', TRUE),
(12, '0562 Becker Street', 'APT J2', 'Clearwater', 'Florida', '33758', TRUE),
(20, '8 Shopko Terrace', 'APT N5', 'Anniston', 'Alabama', '36205', FALSE),
(7, '4149 Hoffman Way', 'APT R6', 'Plano', 'Texas', '75074', FALSE),
(20, '65520 Mesta Pass', 'APT W3', 'El Paso', 'Texas', '88579', FALSE),
(25, '62966 Manitowish Point', 'APT R4', 'Jamaica', 'New York', '11407', FALSE),
(16, '1 Oxford Street', 'APT D7', 'Houston', 'Texas', '77010', TRUE),
(25, '92236 Merry Alley', 'APT K7', 'Hartford', 'Connecticut', '6183', FALSE),
(30, '084 Canary Place', 'APT B5', 'Lafayette', 'Indiana', '47905', FALSE),
(21, '11670 Westend Circle', 'APT O5', 'Des Moines', 'Iowa', '50393', TRUE),
(25, '6050 Arapahoe Alley', 'APT J7', 'Chico', 'California', '95973', TRUE),
(22, '680 Stang Avenue', 'APT V4', 'San Francisco', 'California', '94132', FALSE),
(19, '74218 Anniversary Trail', 'APT T8', 'Elmira', 'New York', '14905', TRUE),
(4, '649 Monterey Place', 'APT G8', 'Charlotte', 'North Carolina', '28272', TRUE),
(24, '420 Bashford Road', 'APT R8', 'Sacramento', 'California', '95852', FALSE),
(10, '8 Nova Lane', 'APT W1', 'Fort Worth', 'Texas', '76192', FALSE),
(4, '2088 Summer Ridge Place', 'APT Z5', 'Saint Paul', 'Minnesota', '55123', TRUE),
(6, '2873 Russell Circle', 'APT K5', 'Greensboro', 'North Carolina', '27425', TRUE),
(23, '57 Scoville Parkway', 'APT B1', 'Denver', 'Colorado', '80241', TRUE),
(22, '4325 International Park', 'APT Q6', 'Omaha', 'Nebraska', '68197', TRUE),
(24, '2 Burrows Point', 'APT L8', 'Colorado Springs', 'Colorado', '80930', TRUE),
(19, '34 Bowman Lane', 'APT W4', 'Greensboro', 'North Carolina', '27455', FALSE),
(10, '76475 Del Mar Road', 'APT F4', 'San Antonio', 'Texas', '78296', TRUE),
(18, '4950 Westridge Park', 'APT C7', 'Anchorage', 'Alaska', '99522', TRUE),
(24, '2615 Ohio Trail', 'APT E4', 'Minneapolis', 'Minnesota', '55417', FALSE),
(10, '0 Dunning Alley', 'APT K8', 'Los Angeles', 'California', '90055', TRUE),
(9, '2560 Helena Crossing', 'APT Q7', 'Baton Rouge', 'Louisiana', '70836', TRUE),
(4, '3725 Corry Hill', 'APT O3', 'Fort Smith', 'Arkansas', '72916', FALSE),
(22, '16 Shopko Pass', 'APT U4', 'Brooklyn', 'New York', '11205', FALSE),
(6, '635 Burrows Parkway', 'APT Q2', 'Tacoma', 'Washington', '98417', FALSE),
(10, '9075 Pepper Wood Alley', 'APT P6', 'Houston', 'Texas', '77212', TRUE),
(16, '41972 Burning Wood Circle', 'APT I2', 'Baton Rouge', 'Louisiana', '70815', TRUE),
(26, '94 Fremont Center', 'APT D1', 'Seattle', 'Washington', '98185', FALSE),
(30, '68186 Messerschmidt Alley', 'APT A1', 'Tucson', 'Arizona', '85743', TRUE),
(30, '8 Jenifer Junction', 'APT M1', 'Sacramento', 'California', '94286', TRUE),
(20, '24 Spaight Court', 'APT F3', 'Fort Lauderdale', 'Florida', '33355', FALSE),
(10, '1 Cody Terrace', 'APT P7', 'Raleigh', 'North Carolina', '27635', TRUE),
(15, '3 Claremont Hill', 'APT Z4', 'Frankfort', 'Kentucky', '40618', FALSE),
(6, '4298 Spenser Trail', 'APT N3', 'Washington', 'District of Columbia', '20580', FALSE),
(29, '5676 Vahlen Crossing', 'APT V5', 'Birmingham', 'Alabama', '35285', FALSE),
(5, '9 Mandrake Pass', 'APT L4', 'Washington', 'District of Columbia', '20456', TRUE),
(2, '44100 Myrtle Plaza', 'APT J5', 'Sacramento', 'California', '95865', FALSE),
(17, '16267 Mayfield Center', 'APT N5', 'Seattle', 'Washington', '98140', FALSE);

INSERT INTO PAYMENT (PaymentMethod, Amount, Date, Status) 
VALUES
('Apple pay', 777.42, '2020-07-17 07:30:00', 'Failed'),
('Debit Card', 486.94, '2021-12-25 07:02:00', 'Successful'),
('Credit Card', 897.06, '2025-02-07 16:47:00', 'Successful'),
('Debit Card', 616.89, '2022-05-03 17:33:00', 'Successful'),
('Paypal', 442.95, '2021-07-23 08:45:00', 'Pending'),
('Apple pay', 626.36, '2024-09-02 18:22:00', 'Successful'),
('Debit Card', 544.64, '2021-02-17 19:46:00', 'Pending'),
('Credit Card', 95.81, '2024-05-06 01:33:00', 'Pending'),
('Apple pay', 779.93, '2024-05-31 14:09:00', 'Failed'),
('Apple pay', 647.01, '2021-07-11 04:16:00', 'Failed'),
('Apple pay', 834.06, '2020-09-07 00:27:00', 'Failed'),
('Apple pay', 916.73, '2022-06-23 23:21:00', 'Pending'),
('Debit Card', 406.98, '2024-04-24 10:17:00', 'Failed'),
('Debit Card', 261.01, '2025-02-14 16:23:00', 'Pending'),
('Paypal', 507.30, '2022-09-18 14:22:00', 'Successful'),
('Credit Card', 57.94, '2023-06-22 20:13:00', 'Successful'),
('Debit Card', 748.78, '2024-04-15 15:43:00', 'Successful'),
('Debit Card', 196.57, '2022-09-27 00:20:00', 'Pending'),
('Debit Card', 483.10, '2024-01-16 16:17:00', 'Successful'),
('Paypal', 254.42, '2024-11-30 17:50:00', 'Pending'),
('Credit Card', 189.37, '2022-05-26 02:49:00', 'Pending'),
('Credit Card', 224.07, '2022-07-13 12:23:00', 'Pending'),
('Credit Card', 590.89, '2020-10-11 10:24:00', 'Failed'),
('Paypal', 65.32, '2024-02-29 06:55:00', 'Failed'),
('Apple pay', 900.55, '2020-04-04 03:47:00', 'Pending'),
('Debit Card', 427.21, '2023-12-04 12:10:00', 'Pending'),
('Paypal', 744.25, '2024-10-24 05:43:00', 'Successful'),
('Debit Card', 294.52, '2021-02-04 22:35:00', 'Failed'),
('Debit Card', 754.49, '2023-09-14 03:37:00', 'Successful'),
('Debit Card', 50.51, '2022-10-29 07:58:00', 'Pending');

INSERT INTO `ORDER` (UserID, PaymentID, OrderedDate, TotalAmount, OrderStatus, DeliveryStatus, DeliveryDate) VALUES
(14, 4, '2023-01-09 08:50:49', 138.64, 'Pending', 'Pending', '2024-07-07 11:21:55'),
(18, 29, '2023-03-28 21:25:30', 572.29, 'Delivered', 'Delivered', '2021-07-20 08:48:52'),
(11, 27, '2020-10-12 20:13:15', 460.4, 'Cancelled', 'Cancelled', '2022-04-25 06:58:20'),
(15, 25, '2023-05-28 08:50:30', 206.36, 'Shipped', 'Delivered', '2021-08-14 09:42:14'),
(30, 23, '2022-12-11 10:53:18', 250.89, 'Shipped', 'Out for Delivery', '2025-01-20 14:23:27'),
(30, 21, '2024-06-25 05:31:07', 867.22, 'Delivered', 'Delivered', '2020-04-20 09:19:56'),
(28, 19, '2022-09-22 03:58:35', 854.34, 'Pending', 'Pending', '2023-03-17 12:03:06'),
(11, 17, '2022-12-12 19:54:55', 756.97, 'Pending', 'Pending', '2020-10-16 16:07:36'),
(15, 15, '2024-07-29 02:22:58', 215.18, 'Pending', 'Pending', '2023-04-10 20:44:13'),
(23, 13, '2025-03-15 21:48:03', 218.6, 'Cancelled', 'Cancelled', '2023-05-30 12:33:22'),
(28, 11, '2024-05-28 01:13:31', 843.12, 'Delivered', 'Delivered', '2021-04-06 19:57:37'),
(11, 9, '2023-12-04 09:10:09', 623.82, 'Cancelled', 'Cancelled', '2022-10-18 09:59:51'),
(25, 7, '2022-10-26 16:57:18', 390.13, 'Pending', 'Pending', '2023-08-26 15:41:02'),
(7, 5, '2024-07-01 22:15:44', 675.6, 'Pending', 'Pending', '2024-10-29 02:54:31'),
(9, 1, '2024-06-10 00:30:58', 623.81, 'Cancelled', 'Cancelled', '2022-10-06 03:25:51'),
(20, 3, '2021-03-26 06:15:44', 923.07, 'Cancelled', 'Cancelled', '2020-06-19 12:56:11'),
(19, 2, '2024-01-27 22:48:00', 756.17, 'Delivered', 'Delivered', '2021-10-23 14:37:18'),
(8, 6, '2021-10-26 11:10:53', 926.87, 'Cancelled', 'Cancelled', '2021-08-01 20:49:54'),
(24, 8, '2022-11-11 02:50:59', 818.51, 'Pending', 'Pending', '2020-05-17 06:57:30'),
(8, 10, '2024-09-11 00:54:06', 702.08, 'Pending', 'Pending', '2024-12-08 05:26:38'),
(8, 12, '2024-01-20 21:00:26', 364.85, 'Delivered', 'Delivered', '2021-12-16 10:48:27'),
(15, 16, '2021-03-04 14:15:15', 719.67, 'Cancelled', 'Cancelled', '2024-05-22 15:23:40'),
(15, 14, '2023-02-01 04:42:25', 857.06, 'Delivered', 'Delivered', '2020-07-25 22:35:33'),
(24, 18, '2023-02-09 03:43:03', 329.43, 'Shipped', 'Out for Delivery', '2020-08-27 20:30:27'),
(11, 20, '2021-12-22 22:38:09', 702.2, 'Cancelled', 'Cancelled', '2023-08-23 11:27:12'),
(29, 22, '2022-10-08 11:18:24', 700.26, 'Pending', 'Pending', '2024-02-22 06:53:17'),
(25, 24, '2022-12-20 21:43:03', 346.77, 'Cancelled', 'Cancelled', '2023-04-18 10:02:17'),
(18, 26, '2024-08-03 11:01:29', 316, 'Shipped', 'Delivered', '2024-04-08 01:24:57'),
(16, 28, '2021-12-21 21:13:53', 590.41, 'Pending', 'Pending', '2021-12-12 10:45:20'),
(19, 30, '2024-10-05 06:08:16', 156.03, 'Shipped', 'Delivered', '2025-01-10 10:47:23');

INSERT INTO CATEGORY (CategoryName) 
VALUES
('Toys'),
('Accessories'),
('Food');

INSERT INTO PRODUCT (CategoryID, ProductName, Description, Price, Stock) VALUES
(1, 'Puppy Chow Delight', 'A delicious blend of flavors for your furry friend', 77.69, 42),
(1, 'Woof Woof Feast', 'Satisfy your pup''s cravings with this tasty meal', 90.33, 78),
(1, 'Bark Bites Buffet', 'A buffet of treats for your beloved pet', 92.48, 54),
(1, 'Tail Waggin'' Treats', 'Treat your dog to some tail-waggin'' goodness', 21.84, 77),
(1, 'Pawsome Protein Patties', 'Protein-packed patties for your pup''s health', 15.1, 100),
(1, 'Snout Snacks Supreme', 'Supreme snacks for your snout-loving pet', 86.34, 57),
(1, 'Furry Friend Favorites', 'Favorites that your furry friend will love', 54.58, 50),
(1, 'Canine Cuisine Creations', 'Creative cuisine for your canine companion', 82.67, 85),
(1, 'Kibble Kingdom Delights', 'Delightful treats fit for a king', 74.21, 3),
(1, 'Chewy Chompers Combo', 'A combo of chewy goodness for your pup', 4.15, 82),
(2, 'Cozy Pup Blanket', 'Soft fleece blanket to keep your pup warm and cozy', 76.46, 33),
(2, 'Paw-some Leash', 'Durable leash with a comfortable grip for daily walks', 147.79, 98),
(2, 'Snuggle Pup Bed', 'Plush bed with extra padding for ultimate doggie comfort', 110.25, 49),
(2, 'Chewy Bone Toy', 'Tough rubber bone toy for hours of chewing fun', 111.17, 7),
(2, 'Furry Friend Collar', 'Adjustable collar with soft lining for your furry friend’s comfort', 148, 65),
(2, 'Woof-tastic Bowtie', 'Stylish bowtie for a dapper dog look at any occasion', 105.96, 55),
(2, 'Tail Wagging Bandana', 'Lightweight bandana to add flair to your dog’s outfit', 125.79, 51),
(2, 'Pampered Pooch Sweater', 'Warm and snug sweater perfect for chilly days', 147.8, 19),
(2, 'Squeaky Toy Set', 'Set of squeaky toys to keep your pup entertained', 124.87, 31),
(2, 'Doggie Treat Pouch', 'Handy pouch to carry treats during training or walks.', 141.09, 33),
(3, 'Pawsome Chow', 'Nutritious dry food packed with essential vitamins for active dogs', 71.93, 88),
(3, 'Woof Delight', 'Tasty blend of meats and grains to satisfy every pup’s cravings', 47.61, 46),
(3, 'Bark Bites', 'Crunchy bite-sized treats perfect for training or rewards', 54.9, 91),
(3, 'Tail Waggin'' Treats', 'Delicious snacks that keep tails wagging with every bite', 78.43, 11),
(3, 'Puppy Palate Pleasers', 'Gourmet treats made with natural ingredients for picky pups', 37.87, 29),
(3, 'Canine Cuisine', 'Premium dog food crafted for balanced daily nutrition', 42.57, 33),
(3, 'Furry Friend Feast', 'Hearty meal mix designed for your furry friend’s health and happiness', 77.79, 23),
(3, 'Snout Snacks', 'Savory snacks that make every sniff and nibble worthwhile', 57.12, 98),
(3, 'Kibble Kingdom', 'High-quality kibble fit for royalty in every bowl', 23.26, 20),
(3, 'Pup Perfection', 'Wholesome formula delivering complete nourishment for all dog breeds.', 33.11, 46);

INSERT INTO BREED (BreedName) 
VALUES
('Labrador Retriever'),
('German Shepherd'),
('Golden Retriever'),
('French Bulldog'),
('Bulldog'),
('Poodle'),
('Beagle'),
('Rottweiler'),
('Yorkshire Terrier'),
('Boxer'),
('Dachshund'),
('Siberian Husky'),
('Great Dane'),
('Doberman Pinscher'),
('Australian Shepherd'),
('Shih Tzu'),
('Border Collie'),
('Pembroke Welsh Corgi'),
('Chihuahua'),
('Pomeranian'),
('Boston Terrier'),
('Basset Hound'),
('Akita'),
('Belgian Malinois'),
('Weimaraner'),
('Newfoundland'),
('Saint Bernard'),
('Cavalier King Charles Spaniel'),
('Alaskan Malamute'),
('Rhodesian Ridgeback');

INSERT INTO PET (BreedID, PetName, Age, Price) 
VALUES
(29, 'Buddy', 7, 296.76),
(11, 'Bella', 5, 543.05),
(2, 'Max', 2, 609.86),
(4, 'Luna', 4, 485.22),
(4, 'Charlie', 5, 510.24),
(20, 'Daisy', 5, 425.89),
(27, 'Rocky', 6, 791.12),
(13, 'Molly', 2, 229.98),
(17, 'Duke', 2, 312.32),
(29, 'Sadie', 6, 159.76),
(16, 'Bear', 1, 934.72),
(30, 'Zoe', 2, 489.44),
(16, 'Milo', 2, 806.88),
(11, 'Rosie', 3, 481.62),
(21, 'Jack', 2, 131.36),
(24, 'Lily', 6, 741.09),
(8, 'Toby', 1, 826.76),
(6, 'Chloe', 4, 854.00),
(17, 'Leo', 2, 823.01),
(30, 'Ruby', 5, 196.01),
(17, 'Finn', 3, 207.18),
(8, 'Roxy', 2, 668.19),
(20, 'Oscar', 5, 713.54),
(8, 'Penny', 6, 777.18),
(11, 'Zeus', 1, 780.52),
(20, 'Nala', 2, 401.56),
(24, 'Scout', 6, 595.58),
(2, 'Ginger', 7, 293.50),
(10, 'Bruno', 5, 592.89),
(14, 'Stella', 5, 261.45);


INSERT INTO ORDERPRODUCT (OrderID, ProductID, Quantity, TotalItemAmount) 
VALUES
(16, 19, 10, 215.89),
(5, 27, 10, 134.78),
(19, 4, 4, 86.01),
(26, 5, 10, 261.25),
(18, 27, 8, 99.16),
(26, 24, 3, 390.43),
(18, 2, 4, 293.12),
(28, 19, 7, 473.67),
(21, 11, 4, 302.79),
(3, 7, 15, 465.79),
(16, 9, 11, 55.71),
(5, 21, 14, 307.01),
(13, 26, 11, 153.24),
(30, 7, 5, 272.99),
(27, 1, 6, 174.67),
(19, 15, 6, 432),
(3, 25, 3, 124.95),
(18, 28, 18, 176.12),
(18, 8, 7, 475.34),
(22, 19, 14, 223.96),
(18, 1, 11, 373.43),
(15, 27, 1, 202.57),
(15, 2, 2, 261.42),
(19, 29, 18, 94.76),
(25, 13, 20, 255.67),
(22, 2, 12, 432.25),
(25, 22, 9, 195.7),
(4, 18, 9, 101.61),
(26, 16, 8, 492.1),
(30, 10, 2, 171.83);

INSERT INTO ORDERPET (OrderID, PetID, Quantity, TotalItemAmount) 
VALUES
(13, 30, 2, 845.86),
(9, 4, 1, 867.88),
(15, 24, 5, 856.63),
(15, 11, 14, 744.27),
(8, 22, 2, 731.09),
(17, 14, 15, 886.03),
(22, 26, 10, 764.76),
(29, 21, 16, 95.47),
(9, 14, 9, 275.61),
(6, 11, 9, 929.62),
(8, 9, 15, 461.89),
(25, 25, 8, 540.35),
(24, 7, 8, 689.13),
(28, 25, 10, 929.02),
(10, 5, 19, 419.65),
(24, 1, 7, 287.05),
(1, 16, 10, 892.63),
(16, 14, 19, 713.75),
(1, 3, 8, 148.80),
(20, 27, 5, 839.68),
(2, 28, 1, 283.99),
(6, 15, 12, 346.36),
(11, 16, 12, 857.09),
(25, 21, 18, 934.32),
(23, 22, 8, 903.78),
(17, 25, 17, 113.29),
(20, 18, 8, 328.79),
(27, 18, 12, 571.25),
(17, 2, 16, 902.61),
(21, 4, 6, 202.01);


