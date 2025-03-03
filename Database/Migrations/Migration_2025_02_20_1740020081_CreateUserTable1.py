# Generated Migration File

from Database.SchemaMigration import SchemaMigration

class CreateUserTable1(SchemaMigration):
    def up(self) -> list:
        # Add migration logic here
        return [
            """
            CREATE TABLE Construction (
                ConID INT PRIMARY KEY AUTO_INCREMENT,
                工事開始日 DATE,
                工事終了日 DATE,
                工事概算金額 DECIMAL(10, 2),
                工事箇所 VARCHAR(255),
                図面ID INT
            );
            """,
            
            """
            CREATE TABLE 図面テーブル (
                図面ID INT PRIMARY KEY AUTO_INCREMENT,
                version VARCHAR(50),
                Affiliation VARCHAR(255),
                ConID INT
            );
            """,
            
            """
            CREATE TABLE 関連資料テーブル (
                ID INT PRIMARY KEY AUTO_INCREMENT,
                図面ID INT,
                関連資料パス VARCHAR(255)  -- Or BLOB for storing images directly
            );
            """,
            
            """
            CREATE TABLE 部品テーブル (
                部品ID INT PRIMARY KEY AUTO_INCREMENT,
                図面ID INT,
                部品名 VARCHAR(255),
                部品詳細 TEXT
            );
            """,
            
            """
            CREATE TABLE 中間テーブル (
                ID INT PRIMARY KEY AUTO_INCREMENT,
                部品ID INT,
                図面ID INT
            );
            """,
            
            # Adding the ALTER TABLE commands to create foreign keys
                        
            """
            ALTER TABLE 図面テーブル 
            ADD FOREIGN KEY (ConID) REFERENCES Construction(ConID);
            """,
            
            """
            ALTER TABLE 関連資料テーブル 
            ADD FOREIGN KEY (図面ID) REFERENCES 図面テーブル(図面ID);
            """,
            
            """
            ALTER TABLE 部品テーブル 
            ADD FOREIGN KEY (図面ID) REFERENCES 図面テーブル(図面ID);
            """,
            
            """
            ALTER TABLE 中間テーブル 
            ADD  FOREIGN KEY (部品ID) REFERENCES 部品テーブル(部品ID),
            ADD  FOREIGN KEY (図面ID) REFERENCES 図面テーブル(図面ID);
            """

        ]

    def down(self) -> list:
        # Add rollback logic here
        return [
            "ALTER TABLE Construction DROP FOREIGN KEY FK_Construction_図面ID;",
            "ALTER TABLE 図面テーブル DROP FOREIGN KEY FK_図面テーブル_ConID;",
            "ALTER TABLE 関連資料テーブル DROP FOREIGN KEY FK_関連資料_図面ID;",
            "ALTER TABLE 部品テーブル DROP FOREIGN KEY FK_部品テーブル_図面ID;",
            "ALTER TABLE 中間テーブル DROP FOREIGN KEY FK_中間テーブル_部品ID;",
            "ALTER TABLE 中間テーブル DROP FOREIGN KEY FK_中間テーブル_図面ID;",
            "DROP TABLE IF EXISTS 中間テーブル;",
            "DROP TABLE IF EXISTS 部品テーブル;",
            "DROP TABLE IF EXISTS 関連資料テーブル;",
            "DROP TABLE IF EXISTS 図面記載テーブル;",
            "DROP TABLE IF EXISTS 図面テーブル;",
            "DROP TABLE IF EXISTS Construction;"

        ]
