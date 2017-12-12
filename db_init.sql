CREATE DATABASE `starcraft`;

CREATE TABLE IF NOT EXISTS `starcraft`.`players` (
  `id`          INT(11)           NOT NULL AUTO_INCREMENT,
  `battletag`   VARCHAR(32)       NOT NULL,
  `server`      ENUM('us','eu')   NOT NULL,
  `p_league`    VARCHAR(13)       NULL DEFAULT 'Unranked',
  `p_mmr`       INT(10)           UNSIGNED DEFAULT NULL,
  `p_games`     INT(10)           UNSIGNED DEFAULT NULL,
  `r_league`    VARCHAR(13)       NULL DEFAULT 'Unranked',
  `r_mmr`       INT(10)           UNSIGNED DEFAULT NULL,
  `r_games`     INT(10)           UNSIGNED DEFAULT NULL,
  `t_league`    VARCHAR(13)       NULL DEFAULT 'Unranked',
  `t_mmr`       INT(10)           UNSIGNED DEFAULT NULL,
  `t_games`     INT(10)           UNSIGNED DEFAULT NULL,
  `z_league`    VARCHAR(13)       NULL DEFAULT 'Unranked',
  `z_mmr`       INT(10)           UNSIGNED DEFAULT NULL,
  `z_games`     INT(10)           UNSIGNED DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE = InnoDB DEFAULT CHARSET = latin1;

CREATE TABLE IF NOT EXISTS `starcraft`.`ladders` (
  `id`          INT(11)           NOT NULL,
  `server`      ENUM('us','eu')   NOT NULL,
  `league`      VARCHAR(13)       NOT NULL,
  `division`    INT(1)            UNSIGNED NOT NULL,
  `floor`       INT(4)            NOT NULL            COMMENT 'lowest MMR in division',
  `ceiling`     INT(4)            NOT NULL            COMMENT 'highest MMR in division',
  PRIMARY KEY (`id`)
) ENGINE = InnoDB DEFAULT CHARSET = latin1;