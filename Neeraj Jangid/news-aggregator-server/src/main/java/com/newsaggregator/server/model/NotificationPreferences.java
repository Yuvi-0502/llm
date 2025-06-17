package com.newsaggregator.server.model;

import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.util.HashSet;
import java.util.Set;

@Data
@Entity
@Table(name = "notification_preferences")
@NoArgsConstructor
@AllArgsConstructor
public class NotificationPreferences {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @OneToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", nullable = false)
    private User user;

    @ManyToMany
    @JoinTable(
        name = "notification_preferences_categories",
        joinColumns = @JoinColumn(name = "preference_id"),
        inverseJoinColumns = @JoinColumn(name = "category_id")
    )
    private Set<Category> categories = new HashSet<>();

    @ElementCollection
    @CollectionTable(name = "notification_keywords", joinColumns = @JoinColumn(name = "preference_id"))
    @Column(name = "keyword")
    private Set<String> keywords = new HashSet<>();

    @Column(name = "email_notifications_enabled")
    private boolean emailNotificationsEnabled = true;

    @Column(name = "push_notifications_enabled")
    private boolean pushNotificationsEnabled = true;
} 