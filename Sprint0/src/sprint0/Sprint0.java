package sprint0;

import javax.swing.JFrame;
import javax.swing.JLabel;

import java.awt.BorderLayout;
import java.awt.GridLayout;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

import javax.swing.*;

public class Sprint0 extends JFrame {
	
//	private JLabel input; 
	private JTextField input = new JTextField(20); 
	private JButton button = new JButton ("Submit"); 
	private JPanel display = new JPanel(new GridLayout(0,1));
	private Connection connection; 
	
	public Sprint0() {
		
		// Set up the display
		setTitle("Enter a name");
		setSize(300, 200);
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		
		// Initialize the database connection
		initializeDatabase();
		

		JPanel panel = new JPanel();
		panel.setLayout(new BorderLayout());
		panel.add(input, BorderLayout.NORTH);
		panel.add(button, BorderLayout.CENTER);
		panel.add(display, BorderLayout.SOUTH);
		
		button.addActionListener(e -> {
			display.removeAll();
			String userInput = input.getText();
			if(!userInput.isEmpty()) {
				saveToDatabase(userInput);
				input.setText("");
				display.add(new JLabel ("Saved: " + userInput));
				display.revalidate();
				display.repaint();
				
				// Display all the entries stored in database in the console 
				printDatabaseContents();
			}
			
		});
		
		add(panel);
	
	}

	private void initializeDatabase() {
		 try { 
			 // Connect to SQLite database (creates it if it doesn't exist) 
			 connection = DriverManager.getConnection("jdbc:sqlite:sprint0.db"); 
			 // Create table if it doesn't exist
			 String createTableQuery = "CREATE TABLE IF NOT EXISTS names (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL)"; 
			 connection.createStatement().execute(createTableQuery); 
			 } catch (SQLException e) {
				 e.printStackTrace();
				 } 		
	}

	private void saveToDatabase(String userInput) {
		
		 String insertQuery = "INSERT INTO names(name) VALUES(?)"; 
		 try (PreparedStatement preparedStatement = connection.prepareStatement(insertQuery)) {
			 preparedStatement.setString(1, userInput);
			 preparedStatement.executeUpdate(); 
		 } catch (SQLException e) { 
			 e.printStackTrace();
			 }
		 
	
	
	}
	
	public void printDatabaseContents() {
	    String query = "SELECT * FROM names";
	    try (Statement stmt = connection.createStatement();
	         ResultSet rs = stmt.executeQuery(query)) {

	        System.out.println("Database Contents:");
	        while (rs.next()) {
	            int id = rs.getInt("id");
	            String name = rs.getString("name");
	            System.out.println("ID: " + id + ", Name: " + name);
	        }
	    } catch (SQLException e) {
	        e.printStackTrace();
	    }
	}
	public static void main(String[] args) { 
		SwingUtilities.invokeLater(() -> { Sprint0 frame = new Sprint0(); 
		frame.setVisible(true); }); 
		}  


}
	
