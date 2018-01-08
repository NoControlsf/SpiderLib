CREATE TABLE shfy_list(
id VARCHAR(100),
caseNumber VARCHAR(200),
title VARCHAR(300),
docType VARCHAR(100),
actionCause VARCHAR(500),
undertakeDept VARCHAR(300),
rank VARCHAR(100),
closingTime VARCHAR(20)
);


CREATE TABLE shfy_detail(
id VARCHAR(100),
court VARCHAR(200),
docDetailType VARCHAR(100),
docCaseNumber VARCHAR(300),
doc TEXT,
other VARCHAR(500)
);