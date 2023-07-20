CREATE TABLE `Metals`
(
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `metal` NVARCHAR(160) NOT NULL,
    `price` NUMERIC(5,2) NOT NULL
);

CREATE TABLE `Styles`
(
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `style` NVARCHAR(160) NOT NULL,
    `price` NUMERIC(5,2) NOT NULL
);

CREATE TABLE `Sizes`
(
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `carets` NUMERIC(5,2) NOT NULL,
    `price` NUMERIC(5,2) NOT NULL
);

CREATE TABLE `Orders`
(
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `metal_id` INTEGER NOT NULL,
    `style_id` INTEGER NOT NULL,
    `size_id` INTEGER NOT NULL,
    `jewelry_id` INTEGER NOT NULL,
    `time_stamp` TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(`metal_id`) REFERENCES `Metals`(`id`),
    FOREIGN KEY(`style_id`) REFERENCES `Styles`(`id`),
    FOREIGN KEY(`size_id`) REFERENCES `Sizes`(`id`)
);


INSERT INTO `Metals` VALUES (null, 'Sterling Silver', 12.42);
INSERT INTO `Metals` VALUES (null, '14K Gold', 736.4);
INSERT INTO `Metals` VALUES (null, '24K Gold', 1258.9);
INSERT INTO `Metals` VALUES (null, 'Platinum', 795.45);
INSERT INTO `Metals` VALUES (null, 'Palladium', 1241);

INSERT INTO `Styles` VALUES (null, 'Classic', 500);
INSERT INTO `Styles` VALUES (null, 'Modern', 710);
INSERT INTO `Styles` VALUES (null, 'Vintage', 965);

INSERT INTO `Sizes` VALUES (null, 0.5, 405);
INSERT INTO `Sizes` VALUES (null, 0.75, 782);
INSERT INTO `Sizes` VALUES (null, 1, 1470);
INSERT INTO `Sizes` VALUES (null, 1.5, 1997);
INSERT INTO `Sizes` VALUES (null, 2, 3638);

INSERT INTO `Orders` VALUES (null, 1, 2, 2, 1, 0);
INSERT INTO `Orders` VALUES (null, 1, 1, 3, 2, 0);
INSERT INTO `Orders` VALUES (null, 5, 5, 3, 3, 0);
INSERT INTO `Orders` VALUES (null, 5, 3, 5, 1, 0);
INSERT INTO `Orders` VALUES (null, 2, 2, 2, 2, 0);
INSERT INTO `Orders` VALUES (null, 1, 3, 4, 1, 0);


SELECT
    o.id,
    o.time_stamp,
    o.size_id,
    o.style_id,
    o.metal_id,
    m.metal,
    m.price,
    st.style,
    st.price,
    s.carets,
    s.price
FROM `Orders` o
JOIN Metals m
    ON m.id = o.metal_id
JOIN Styles st
    ON st.id = o.style_id
JOIN Sizes s
    ON s.id = o.size_id;

    DROP TABLE Orders;