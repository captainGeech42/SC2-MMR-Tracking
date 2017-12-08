CREATE DATABASE `starcraft`;

CREATE TABLE IF NOT EXISTS `starcraft`.`players` (
  `battletag`   VARCHAR(32)       NOT NULL,
  `server`      enum('us','eu')   NOT NULL,
  `p_league`    varchar(13)       DEFAULT NULL,
  `p_mmr`       int(10)           unsigned DEFAULT NULL,
  `r_league`    varchar(13)       DEFAULT NULL,
  `r_mmr`       int(10)           unsigned DEFAULT NULL,
  `t_league`    varchar(13)       DEFAULT NULL,
  `t_mmr`       int(10)           unsigned DEFAULT NULL,
  `z_league`    varchar(13)       DEFAULT NULL,
  `z_mmr`       int(10)           unsigned DEFAULT NULL,
  PRIMARY KEY (`battletag`)
) ENGINE = InnoDB DEFAULT CHARSET = latin1;

CREATE TABLE IF NOT EXISTS `starcraft`.`ladders` (
  `id`          int(11)           NOT NULL,
  `server`      enum('us','eu')   NOT NULL,
  `league`      varchar(13)       NOT NULL,
  `division`    int(1)            unsigned NOT NULL,
  `floor`       int(4)            NOT NULL            COMMENT 'lowest MMR in division',
  `ceiling`     int(4)            NOT NULL            COMMENT 'highest MMR in division',
  PRIMARY KEY (`id`)
) ENGINE = InnoDB DEFAULT CHARSET = latin1;