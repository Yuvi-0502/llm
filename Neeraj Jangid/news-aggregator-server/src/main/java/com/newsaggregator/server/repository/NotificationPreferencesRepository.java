package com.newsaggregator.server.repository;

import com.newsaggregator.server.model.NotificationPreferences;
import com.newsaggregator.server.model.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;
import java.util.List;
import java.util.Optional;

@Repository
public interface NotificationPreferencesRepository extends JpaRepository<NotificationPreferences, Long> {
    Optional<NotificationPreferences> findByUser(User user);
    
    @Query("SELECT np FROM NotificationPreferences np " +
           "JOIN np.categories c " +
           "WHERE c.id = :categoryId AND np.emailNotificationsEnabled = true")
    List<NotificationPreferences> findByCategoryIdAndEmailEnabled(@Param("categoryId") Long categoryId);
    
    @Query("SELECT np FROM NotificationPreferences np " +
           "WHERE np.emailNotificationsEnabled = true AND " +
           "EXISTS (SELECT k FROM np.keywords k WHERE " +
           "LOWER(:content) LIKE LOWER(CONCAT('%', k, '%')))")
    List<NotificationPreferences> findByKeywordsAndEmailEnabled(@Param("content") String content);
} 