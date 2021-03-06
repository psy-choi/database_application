DROP TABLE beloging_church;
DROP TABLE church_officer;
DROP TABLE person;
DROP TABLE takes;
DROP TABLE penalty;
DROP TABLE account;

CREATE TABLE belonging_church
(
	belonging varchar(50) PRIMARY KEY,
	location varchar(50) NOT NULL,
	denomination varchar(15) NOT NULL,
	explanation text
);


CREATE TABLE church_officer
(
	belonging varchar(50),
	officer varchar(50),
	pray_time INT NOT NULL,
	bible_page INT NOT NULL,
	QT boolean NOT NULL,
	FOREIGN KEY (belonging) REFERENCES belonging_church(belonging)
	ON DELETE CASCADE,
	PRIMARY KEY(belonging, officer)
);


CREATE TABLE person
(
	ID varchar(15) PRIMARY KEY,
	password varchar(50) NOT NULL,
	name varchar(50) NOT NULL,
	belonging varchar(50),
	officer varchar(50),
	age smallint NOT NULL,
	all_fine INT DEFAULT 0,
	FOREIGN KEY (belonging, officer) REFERENCES church_officer(belonging, officer) ON DELETE CASCADE
);




CREATE TABLE takes
(	
	ID varchar(15),
	belonging varchar(50),
	officer varchar(50),
	date date NOT NULL,
	today_pray INT NOT NULL,
	today_bible INT NOT NULL,
	today_QT boolean NOT NULL,
	fine INT DEFAULT 0,
	FOREIGN KEY (ID) REFERENCES person(ID) ON DELETE CASCADE,
	PRIMARY KEY (ID, DATE)	
);



CREATE TABLE penalty
(
	belonging varchar(50),
	officer varchar(50),
	one INT NOT NULL,
	two INT NOT NULL,
	three INT NOT NULL,
	FOREIGN KEY (belonging, officer) REFERENCES church_officer(belonging, officer) ON DELETE CASCADE
);



CREATE TABLE account
(	
	belonging varchar(50),
	purpose varchar(50),
	account text NOT NULL,
	FOREIGN KEY (belonging) REFERENCES belonging_church(belonging)
	ON DELETE CASCADE,
	PRIMARY KEY (belonging, purpose)	
);


INSERT INTO belonging_church VALUES('REAL_BEUATIFUL_CHURCH', '수원', '장로회 합동', '저희 교회는 수원에 위치한 교회로서, 탑동과 구운동에
복음을 전하기 위해서 세워진 교회입니다.');
INSERT INTO church_officer VALUES('REAL_BEUATIFUL_CHURCH', '일반성도', 10, 1, true);
INSERT INTO church_officer VALUES('REAL_BEUATIFUL_CHURCH', '집사', 20, 3, true);
INSERT INTO church_officer VALUES('REAL_BEUATIFUL_CHURCH', '권사', 30, 5, true);
INSERT INTO church_officer VALUES('REAL_BEUATIFUL_CHURCH', '장로', 30, 5, true);
INSERT INTO church_officer VALUES('REAL_BEUATIFUL_CHURCH', '목사', 60, 5, true);
INSERT INTO person VALUES('chlrltjd5263', 'choi0924', '최기성', 'REAL_BEUATIFUL_CHURCH', '일반성도', 24);
INSERT INTO person VALUES('asiaprince', 'han123', '한성진', 'REAL_BEUATIFUL_CHURCH', '권사', 32);
INSERT INTO person VALUES('daniel_choi', 'choi123456', '최경환', 'REAL_BEUATIFUL_CHURCH', '집사', 24);
INSERT INTO penalty VALUES('REAL_BEUATIFUL_CHURCH', '일반성도', 100, 200, 300);
INSERT INTO penalty VALUES('REAL_BEUATIFUL_CHURCH', '집사', 200, 300, 500);
INSERT INTO penalty VALUES('REAL_BEUATIFUL_CHURCH', '권사', 300, 600, 700);
INSERT INTO penalty VALUES('REAL_BEUATIFUL_CHURCH', '장로', 500, 1000, 1500);
INSERT INTO penalty VALUES('REAL_BEUATIFUL_CHURCH', '목사', 1000, 2000, 3000);
INSERT INTO account VALUES('REAL_BEUATIFUL_CHURCH', '헌금', '신* 110-******-*******');
INSERT INTO account VALUES('REAL_BEUATIFUL_CHURCH', '벌금', '기* 340-******-*******');