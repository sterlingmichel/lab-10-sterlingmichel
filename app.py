from flask import Flask, url_for, render_template
import psycopg2
from psycopg2.extras import RealDictCursor

# define the application
app = Flask(__name__)

# define the connection string
connString = "postgresql://sterlingmichel:va29PtHWE7dGaEAuJ8ceNPAObF7Esrbp@dpg-cshq6t68ii6s73bjvcpg-a.oregon-postgres.render.com/sterlingmichel_db"


@app.route("/")
def index():
    return """
        <style>
            button {
                border: 1px #ccc solid;
                border-radius: 10px;
                padding: 4px;
            }
        </style>
        <script type="text/javascript">
            function addMsg(msg) {
                document.getElementById('msg').innerHTML = msg;
            }

            function runRoute(url) {
                fetch(url)
                .then((result) => {
                    console.log("==", result)
                    result
                        .json()
                        .then((data) => {
                            if(typeof(data.info) === 'object') {
                                addMsg(JSON.stringify(data.info, null, 1));
                            } else {
                                addMsg(data.info);
                            }
                        })
                        .catch((err) => {
                           addMsg("Server Connection Error. Message was: " + err);
                        })
                })
                .catch((err) => {
                    addMsg("Server Connection Error. Message was: " + err);
                });
            }
        </script>

        <p>Hello World</p>
        <p>please trigger the action below</p>

        <button onClick="runRoute('/about')">Author Information</button>
        &nbsp;
        <button onClick="runRoute('/db_test')">Test DB Connection</button>
        &nbsp;
        <button onClick="runRoute('/db_create')">Create DB Schema</button>
        &nbsp;
        <button onClick="runRoute('/db_drop')">Drop DB Schema</button>
        &nbsp;
        <button onClick="runRoute('/db_select)">Select DB Schema</button>
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

    try:
        # now execute the query
        cur.execute(
            """
                INSERT INTO Basketball (Id, First, Last, City, Name, Number)
                Values
                    (1, 'Jayson', 'Tatum', 'Boston', 'Celtics', 0),
                    (2, 'Stephen', 'Curry', 'San Francisco', 'Warriors', 30),
                    (3, 'Nikola', 'Jokic', 'Denver', 'Nuggets', 15),
                    (4, 'Kawhi', 'Leonard', 'Los Angeles', 'Clippers', 2),
                    (5, 'Lebron', 'Jame', 'Los Angeles', 'Lakers', 6),
                    (6, 'Kevin', 'Durant', 'Phoenix', 'Suns', 17),
                    (7, 'Duane', 'Wade', 'Miami', 'Heat', 10);
            """
        )

        # Save the update
        conn.commit()

        # set the message
        info = "Adding reocrd to Basketball table successfull"
    except Exception as err:
        info = str(err)

    cur.close()
    conn.close()
    return {"info": info}


@app.route("/db_view")
def db_view():
    # Hard coded the connection string
    conn = psycopg2.connect(connString)

    # Establish a cursor
    cur = conn.cursor(cursor_factory=RealDictCursor)

    try:
        # now execute the query
        cur.execute(
            """
                SELECT b.Id, b.First, b.Last, b.City, b.Name, b.Number 
                FROM Basketball b
                ORDER BY b.Last Asc, b.First Asc;
            """
        )

        # Query the table
        records = cur.fetchall()

        # set the message
        info = "Select record to Basketball table successfull"
    except Exception as err:
        info = str(err)
        records = []

    cur.close()
    conn.close()

    return {"info": info, "records": records}

@app.route("/db_select")
def db_select():
    # grab the
    record_fnc = db_view()

    out = ""
    if len(record_fnc['records']) > 0:
        # store the rows
        tr = []

        tr.append('<thead>')
        [ tr.append('<th>' + x + '</th>') for x in record_fnc['records'][0]]
        tr.append('</thead>')

        tr.append('<tbody>')
        for x in range(0, len(record_fnc['records'])):
            tr.append("<tr>")
            for (col, val) in record_fnc['records'][x].items():
                tr.append("<td>" + str(val) + "</td>")
            tr.append("</tr>")
        tr.append('</tbody')

        out = '<table border="1" cellpadding="1" cellspacing="1" width="100%">' + ''.join(tr) + '</table>'

    return out