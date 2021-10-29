from db_points import drop_tables, create_tables


def prepare_db():
    drop_tables()
    create_tables()
    print("db is prepared")


if __name__ == "__main__":
    prepare_db()


