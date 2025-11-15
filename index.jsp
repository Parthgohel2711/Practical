<%@page import = "java.sql.*;" %>
<%@page contentType="text/html" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>Login Form</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" />

        <style>
            body {
                background: #f0f2f5;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }

            .form-container {
                background: white;
                padding: 30px 40px;
                border-radius: 12px;
                box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
                width: 350px;
            }

            h2 {
                text-align: center;
                margin-bottom: 25px;
                color: #333;
            }

            .btn-primary {
                width: 100%;
                padding: 10px;
                font-weight: 600;
                font-size: 1.1rem;
            }

            .error-msg {
                color: black;
                margin-top: 10px;
                text-align: center;
            }
        </style>
    </head>
    <body>

        <div class="form-container">
            <h2>Login Page</h2>

            <form method="POST">
                <div class="mb-3">
                    <input required type="text" class="form-control" name="nm" id="name" placeholder="Enter Username" />
                </div>
                <div class="mb-3">
                    <input required type="password" class="form-control" name="pwd" id="password" placeholder="Enter Password" />
                </div>
                <button type="submit" class="btn btn-primary">LogIn</button>
            </form>

            <!-- error message will appear here -->
            <div id="errorBox">
                <% 
                    String nm = request.getParameter("nm");
                    String pwd = request.getParameter("pwd");

                    if (nm != null && pwd != null) {
                        Connection conn = null;
                        PreparedStatement pst = null;
                        ResultSet rs = null;

                        try {
                            Class.forName("com.mysql.cj.jdbc.Driver");
                            conn = DriverManager.getConnection("jdbc:mysql://localhost:3306/clg?useSSL=false", "root", "");

                            String q = "SELECT * FROM user WHERE unm=? AND pwd=?";
                            pst = conn.prepareStatement(q);
                            pst.setString(1, nm);
                            pst.setString(2, pwd);

                            rs = pst.executeQuery();

                            if (rs.next()) {
                                response.sendRedirect("Welcome.jsp");
                            } else {
                                out.println("<p class='error-msg'>Invalid username or password!</p>");
                            }

                        } catch (Exception e) {
                            e.printStackTrace();
                        } finally {
                            try {
                                if (rs != null) rs.close();
                                if (pst != null) pst.close();
                                if (conn != null) conn.close();
                            } catch (SQLException ex) {
                                ex.printStackTrace();
                            }
                        }
                    }
                %>
            </div>
        </div>
    </body>
</html>
