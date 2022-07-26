CREATE TABLE "type" (
  "id" TEXT NOT NULL,
  "aliases" TEXT,
  "manufacturer" TEXT,
  "manufactureruri" TEXT,
  "modelnumber" TEXT,
  "modelsupporturi" TEXT,
  "modelinformationuri" TEXT,
  "name" TEXT,
  "tags" TEXT,
  "macaddresses" TEXT,
  "behaviour" TEXT,
  "parents" TEXT,
  "children" TEXT,
 PRIMARY KEY("id")
)

CREATE TABLE "firmware" (
  "id" TEXT NOT NULL,
  "type" TEXT NOT NULL,
  "versions" TEXT
  "behaviour" TEXT
)

CREATE TABLE "behaviour" (
  "id" TEXT NOT NULL,
  "ruleid" TEXT NOT NULL,
  "rulename" TEXT,
  "malicious" BOOLEAN DEFAULT 0,
  PRIMARY KEY("id","ruleid")
)

CREATE TABLE "behaviour_eth" (
  "ruleid" TEXT NOT NULL,
  "sourcemac" TEXT,
  "sourcemacmask" TEXT,
  "destinationmac" TEXT,
  "destinationmacmask" TEXT,
  "ethertype" NUMERIC NOT NULL,
  PRIMARY KEY("ruleid")
)

CREATE TABLE "behaviour_ip4" (
  "ruleid" TEXT NOT NULL,
  "sourceip4" TEXT,
  "destinationip4" TEXT,
  "sourcednsname" TEXT,
  "destinationdnsname" TEXT,
  "protocol" NUMERIC NOT NULL,
  "ihl" NUMERIC,
  "tos" NUMERIC,
  "ttl" NUMERIC,
  "offset" NUMERIC,
  "length" NUMERIC,
  PRIMARY KEY("ruleid")
)

CREATE TABLE "behaviour_ip6" (
  "ruleid" TEXT NOT NULL,
  "sourceip6" TEXT,
  "destinationip6" TEXT,
  "sourcednsname" TEXT,
  "destinationdnsname" TEXT,
  "protocol" NUMERIC NOT NULL,
  "ttl" NUMERIC,
  "flowlabel" NUMERIC,
  "length" NUMERIC,
  PRIMARY KEY("ruleid")
)

CREATE TABLE "behaviour_tcp" (
  "ruleid" TEXT NOT NULL,
  "sourceport" INTEGER,
  "destinationport" INTEGER,
  PRIMARY KEY("ruleid")
)

CREATE TABLE "behaviour_udp" (
  "ruleid" TEXT NOT NULL,
  "sourceport" INTEGER,
  "destinationport" INTEGER,
  PRIMARY KEY("ruleid")
)

CREATE TABLE "behaviour_icmp" (
  "ruleid" TEXT NOT NULL,
  "type" INTEGER,
  "code" INTEGER,
  PRIMARY KEY("ruleid")
)
