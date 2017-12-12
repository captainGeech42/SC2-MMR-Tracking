CREATE DATABASE `starcraft`;

CREATE TABLE IF NOT EXISTS `starcraft`.`players` (
  `id`          INT(11)           NOT NULL AUTO_INCREMENT,
  `battletag`   VARCHAR(32)       NOT NULL,
  `server`      ENUM('us','eu')   NOT NULL,
  `p_league`    VARCHAR(13)       NOT NULL DEFAULT 'Unranked',
  `p_mmr`       INT(10)           UNSIGNED DEFAULT 0,
  `p_games`     INT(10)           UNSIGNED DEFAULT 0,
  `r_league`    VARCHAR(13)       NOT NULL DEFAULT 'Unranked',
  `r_mmr`       INT(10)           UNSIGNED DEFAULT 0,
  `r_games`     INT(10)           UNSIGNED DEFAULT 0,
  `t_league`    VARCHAR(13)       NOT NULL DEFAULT 'Unranked',
  `t_mmr`       INT(10)           UNSIGNED DEFAULT 0,
  `t_games`     INT(10)           UNSIGNED DEFAULT 0,
  `z_league`    VARCHAR(13)       NOT NULL DEFAULT 'Unranked',
  `z_mmr`       INT(10)           UNSIGNED DEFAULT 0,
  `z_games`     INT(10)           UNSIGNED DEFAULT 0,
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