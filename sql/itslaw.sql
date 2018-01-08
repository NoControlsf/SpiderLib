CREATE TABLE itslaw_list(
id VARCHAR(50),
title VARCHAR(300),
caseType VARCHAR(50),
publishBatch VARCHAR(200),
judgementType VARCHAR(50),
courtName VARCHAR(200),
caseNumber VARCHAR(200),
judgementDate VARCHAR(10),
courtOpinion VARCHAR(500),
publishDate VARCHAR(10),
publishType VARCHAR(10)
);

CREATE TABLE itslaw_detail(
id VARCHAR(50),
title VARCHAR(300),
typeText VARCHAR(100),
subParagraphs TEXT
);