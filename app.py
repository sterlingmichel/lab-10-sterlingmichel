from flask import Flask, url_for, render_template
import psycopg2


app = Flask(__name__)

connString = "postgresql://sterlingmichel:va29PtHWE7dGaEAuJ8ceNPAObF7Esrbp@dpg-cshq6t68ii6s73bjvcpg-a.oregon-postgres.render.com/sterlingmichel_db"


@app.route("/")
def index():
    return """
        <script type="text/javascript">
            function runRoute(url) {
                fetch(url)
                .then((result) => {
                    result
                        .json()
                        .then((data) => {
                            if(typeof(data.info) === 'object') {
                                document.getElementById('msg').innerHTML = JSON.stringify(data.info, null, 1);
                            } else {
                                document.getElementById('msg').innerHTML = data.info;
                            }
                        })
                        .catch((err) => {
                            document.getElementById('msg').innerHTML = "Server Connection Error. Message was: ", err;
                        })
                })
                .catch((err) => {
                    document.getElementById('msg').innerHTML = "Server Connection Error. Message was: ", err;
                });
            }
        </script>
        <p>Hello World</p>
        <p>please trigger the action below</p>
        <button onClick="runRoute('/about')">Author Information</button>
        <button onClick="runRoute('/db_test')">Test DB Connection</button>
        &nbsp;
        <button onClick="runRoute('/db_create')">Create DB Schema Basketball</button>
        &nbsp;
        <button onClick="runRoute('/db_drop')">Drop DB Schema Basketball</button>
        <p>
            <div>Status: <span id="msg"></span></div>
        </p>
    """


@app.route("/about")
def about():
    return {
        "info": {
            "Your name": "Sterling Michel",
            "CU ID": "CU8072",
            "GitHub Username": "sterlingmichel",
            "hours to complete lab": "3 hrs",
        }
    }


# Add the 5 methods test required
@app.route("/db_test")
def db_test():
    # Hard coded the connection string
    conn = psycopg2.connect(connString)

    # close the active session
    conn.close()
    return {"info": "Database connection was successfull"}


@app.route("/db_create")
def db_create():
    # Hard coded the connection string
    conn = psycopg2.connect(connString)

    # Establish a cursor
    cur = conn.cursor()

    # now execute the query
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS public.Basketball
        (
            Id bigint NOT NULL,
            First character varying(100) COLLATE pg_catalog."default" NOT NULL,
            Last character varying(100) COLLATE pg_catalog."default" NOT NULL,
            City character varying(100) COLLATE pg_catalog."default" NOT NULL,
            Name character varying(100) COLLATE pg_catalog."default" NOT NULL,
            Number bigint NOT NULL,
            CONSTRAINT Basketball_pkey PRIMARY KEY (Id)
        )
    """
    )

    # Save the update
    conn.commit()

    # close the active session
    conn.close()
    return {"info": "Basketball table was successfull created"}


@app.route("/db_drop")
def db_drop():
    # Hard coded the connection string
    conn = psycopg2.connect(connString)

    # Establish a cursor
    cur = conn.cursor()

    # now execute the query
    cur.execute(
        """
        DROP TABLE IF EXISTS public.Basketball;
    """
    )

    # Save the update
    conn.commit()

    conn.close()
    return {"info": "Basketball table was dropped"}


@app.route("/db_insert")
def db_insert():
    # Hard coded the connection string
    conn = psycopg2.connect(connString)

    # Establish a cursor
    cur = conn.cursor()

    # now execute the query
    cur.execute(
        """
        INSERT INTO Basketball (First, Last, City, Name, Number)
        Values
            ('Jayson', 'Tatum', 'Boston', 'Celtics', 0),
            ('Stephen', 'Curry', 'San Francisco', 'Warriors', 30),
            ('Nikola', 'Jokic', 'Denver', 'Nuggets', 15),
            ('Kawhi', 'Leonard', 'Los Angeles', 'Clippers', 2),
            ('Lebron', 'Jame', 'Los Angeles', 'Lakers', 6),
            ('Kevin', 'Durant', 'Phoenix', 'Suns', 17),
            ('Duane', 'Wade', 'Miami', 'Heat', 10);
    """
    )

    # Save the update
    conn.commit()

    cur.close()
    conn.close()
    return {"info": "Adding reocrd to Basketball table successfull"}


@app.route("/db_select")
def db_select():
    # Hard coded the connection string
    conn = psycopg2.connect(connString)

    # Establish a cursor
    cur = conn.cursor()

    # now execute the query
    cur.execute(
        """
        SELECT b.First, b.Last, b.City, b.Name, b.Number From Basketball b
        ORDER BY c.last asc, c.first asc;
    """
    )

    # Save the update
    conn.fet()

    cur.close()
    conn.close()
    return {"info": "Adding reocrd to Basketball table successfull"}
