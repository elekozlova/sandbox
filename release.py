from db_points import drop_table, create_table


def prepare_db():
    drop_table()
    create_table()
    print("db is prepared")


if __name__ == "__main__":
    prepare_db()


