package com.newsaggregator.server.service;

import com.newsaggregator.server.model.User;
import org.springframework.security.core.userdetails.UserDetailsService;
import java.util.Optional;

public interface UserService extends UserDetailsService {
    User createUser(User user);
    Optional<User> getUserById(Long id);
    Optional<User> getUserByUsername(String username);
    Optional<User> getUserByEmail(String email);
    boolean existsByUsername(String username);
    boolean existsByEmail(String email);
    void updateUser(User user);
    void deleteUser(Long id);
} 