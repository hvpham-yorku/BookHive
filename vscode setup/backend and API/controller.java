// AuthController.java
package com.example.pro;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/auth")
public class controller {

    @PostMapping("/login")
    public String login(@RequestBody login loginRequest) {
        if ("user".equals(loginRequest.getUsername()) && "password".equals(loginRequest.getPassword())) {
            return "Login successful!";
        } else {
            return "Invalid credentials";
        }
    }
}
