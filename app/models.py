from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator

class Users(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=20)
    cookie = fields.CharField(max_length=128)
    session_token = fields.CharField(max_length=256)
    created_at = fields.DatetimeField()
    updated_at = fields.DatetimeField()

class Battles(models.Model):
    id = fields.IntField(pk=True)
    user_id = fields.IntField()
    no = fields.IntField(null=True)
    game_mode = fields.CharField(max_length=20, null=True)
    rule = fields.CharField(max_length=20, null=True)
    type = fields.CharField(max_length=20, null=True)
    stage_id = fields.IntField(null=True)

    estimate_x_power = fields.IntField(null=True)
    estimate_gachi_power = fields.IntField(null=True)
    crown_players = fields.CharField(max_length=20, null=True)

    my_team_result = fields.CharField(max_length=20, null=True)
    other_team_result = fields.CharField(max_length=20, null=True)
    my_team_count = fields.IntField(null=True)
    other_team_count = fields.IntField(null=True)

    player_rank = fields.IntField(null=True)
    star_rank = fields.IntField(null=True)
    x_power = fields.FloatField(null=True)
    weapon_paint_point = fields.IntField(null=True)
    s_plus_number = fields.IntField(null=True)
    is_number_reached = fields.IntField(null=True)
    is_x = fields.IntField(null=True)
    number = fields.IntField(null=True)
    name = fields.CharField(max_length=20, null=True)

    start_time = fields.DatetimeField(null=True)
    elapsed_time = fields.IntField(null=True)

    class Meta:
        unique_together=(("user_id", "no"), )


class Players(models.Model):
    id = fields.IntField(pk=True)
    battle_id = fields.IntField()

    nickname = fields.CharField(max_length=128)
    player_rank = fields.IntField()
    star_rank = fields.IntField(null=True)
    principal_id = fields.CharField(max_length=128)
    is_x = fields.IntField(null=True)
    udemae = fields.CharField(max_length=128)
    s_plus_number = fields.IntField(null=True)

    species = fields.CharField(max_length=128)
    style = fields.CharField(max_length=128)

    kill_count = fields.IntField()
    assist_count = fields.IntField()
    death_count = fields.IntField()
    special_count = fields.IntField()
    game_paint_point = fields.IntField()
    sort_score = fields.IntField()

    weapon_id = fields.IntField()
    head_gear_id = fields.IntField()
    clothes_gear_id = fields.IntField()
    shoes_gear_id = fields.IntField()
    head_main_skill_id = fields.IntField()
    head_sub_skill_1_id = fields.IntField(null=True)
    head_sub_skill_2_id = fields.IntField(null=True)
    head_sub_skill_3_id = fields.IntField(null=True)
    clothes_main_skill_id = fields.IntField()
    clothes_sub_skill_1_id = fields.IntField(null=True)
    clothes_sub_skill_2_id = fields.IntField(null=True)
    clothes_sub_skill_3_id = fields.IntField(null=True)
    shoes_main_skill_id = fields.IntField()
    shoes_sub_skill_1_id = fields.IntField(null=True)
    shoes_sub_skill_2_id = fields.IntField(null=True)
    shoes_sub_skill_3_id = fields.IntField(null=True)

User_Pydantic = pydantic_model_creator(Users, name="User")
UserIn_Pydantic = pydantic_model_creator(Users,
                                         name="UserIn",
                                         exclude_readonly=True)

Battle_Pydantic = pydantic_model_creator(Battles, name="Battle")
BattleIn_Pydantic = pydantic_model_creator(Battles,
                                         name="BattleIn",
                                         exclude_readonly=True)
