package com.newsaggregator.server.repository;

import com.newsaggregator.server.model.SavedArticle;
import com.newsaggregator.server.model.User;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.Optional;

@Repository
public interface SavedArticleRepository extends JpaRepository<SavedArticle, Long> {
    Page<SavedArticle> findByUser(User user, Pageable pageable);
    Optional<SavedArticle> findByUserAndArticleId(User user, Long articleId);
    void deleteByUserAndArticleId(User user, Long articleId);
    boolean existsByUserAndArticleId(User user, Long articleId);
} 