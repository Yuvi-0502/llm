package com.newsaggregator.server.repository;

import com.newsaggregator.server.model.Article;
import com.newsaggregator.server.model.Category;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;
import java.time.LocalDateTime;
import java.util.List;

@Repository
public interface ArticleRepository extends JpaRepository<Article, Long> {
    
    Page<Article> findByCategory(Category category, Pageable pageable);
    
    Page<Article> findByPublishedAtBetween(LocalDateTime start, LocalDateTime end, Pageable pageable);
    
    @Query("SELECT a FROM Article a WHERE a.publishedAt BETWEEN :start AND :end AND a.category = :category")
    Page<Article> findByPublishedAtBetweenAndCategory(
        @Param("start") LocalDateTime start,
        @Param("end") LocalDateTime end,
        @Param("category") Category category,
        Pageable pageable
    );
    
    @Query("SELECT a FROM Article a WHERE " +
           "LOWER(a.title) LIKE LOWER(CONCAT('%', :query, '%')) OR " +
           "LOWER(a.description) LIKE LOWER(CONCAT('%', :query, '%')) OR " +
           "LOWER(a.content) LIKE LOWER(CONCAT('%', :query, '%'))")
    Page<Article> searchArticles(@Param("query") String query, Pageable pageable);
    
    @Query("SELECT a FROM Article a WHERE a.publishedAt BETWEEN :start AND :end AND " +
           "(LOWER(a.title) LIKE LOWER(CONCAT('%', :query, '%')) OR " +
           "LOWER(a.description) LIKE LOWER(CONCAT('%', :query, '%')) OR " +
           "LOWER(a.content) LIKE LOWER(CONCAT('%', :query, '%')))")
    Page<Article> searchArticlesWithDateRange(
        @Param("query") String query,
        @Param("start") LocalDateTime start,
        @Param("end") LocalDateTime end,
        Pageable pageable
    );
    
    List<Article> findBySource(String source);
} 