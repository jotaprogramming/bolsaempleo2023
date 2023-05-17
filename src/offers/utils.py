import base64
import sys, codecs
from pprint import pprint

from notifications.signals import notify
from django.contrib.auth.models import User

# from offers.models import Candidatures

POST_STATUS = (
    ("1", "aplicado"),
    ("2", "cancelado"),
    ("3", "rechazado"),
    ("4", "aceptado"),
    ("5", "contratado"),
)

OFFER_STATUS = (
    ("1", "publicada"),
    ("2", "finalizada"),
)


def string_to_base64(sample_string):
    sample_string_bytes = sample_string.encode("ascii")

    base64_bytes = base64.b64encode(sample_string_bytes)
    base64_string = base64_bytes.decode("ascii")
    return base64_string


def base64_to_string(base64_string):
    if "===" in base64_string:
        return ""
    try:
        base64_bytes = base64_string.encode("ascii")

        sample_string_bytes = base64.b64decode(base64_bytes)
        sample_string = sample_string_bytes.decode("ascii")
        return sample_string
    except:
        base64_to_string(f"{base64_string}=")


def get_pk_from_a_slug(self):
    slug = self.kwargs.get("slug", "")
    slug_split = slug.split("-")
    split_pk = slug_split[-1]
    # str_pk = base64_to_string(f"{split_pk}")
    return split_pk


def get_status_name(p_stauts):
    for status in POST_STATUS:
        _id = status[0]
        if _id == p_stauts:
            return status[1]


def send_new_offer_notification(self):
    if self.tags:
        interested_users = User.objects.filter(
            rule_user__usergroup__code="GRA", candidate__offer__tags__in=self.tags
        )
        system_user = User.objects.get(username="system")

        for user in interested_users:
            notify.send(
                sender=system_user,
                recipient=user,
                verb="oferta",
                target=self.object,
                description="Se ha publicado un nuevo empleo que podría interesarte.",
            )


def get_message_to_state(status, candidature, company, candidate):
    candidate_name = candidate.first_name if candidate.first_name else candidate.username
    status_name = get_status_name(status)
    if status == "1":
        return {
            "recipient": candidature.offer.user,
            "verb": status_name,
            "description": f"¡Hola {company}!\n¡Tenemos buenas noticias! Se ha registrado un nuevo candidato interesado en la oferta '{candidature.offer.title}'. Su nombre es {candidate_name}.\nTe sugerimos revisar el perfil y la información proporcionada por este candidato en nuestra plataforma para evaluar su idoneidad y considerarlo en tu proceso de selección.\n¡Te deseamos éxito en tu búsqueda del candidato ideal!",
        }
    elif status == "2":
        return {
            "recipient": candidature.offer.user,
            "verb": status_name,
            "description": f"¡Hola {company}!\nTe informamos que {candidate_name}, quien había sido aceptado en el proceso de selección de la oferta '{candidature.offer.title}', ha decidido cancelar su candidatura.\nLamentamos cualquier inconveniente que esto pueda causar y te invitamos a revisar los demás candidatos que se encuentran en proceso de selección para encontrar al mejor candidato para tu oferta.",
        }
    elif status == "3":
        return {
            "recipient": candidate,
            "verb": status_name,
            "description": f"Lamentamos informarte que no has sido seleccionado para continuar en el proceso de contratación de la oferta '{candidature.offer.title}'. Queremos agradecerte por tu interés y tiempo invertido en nuestra bolsa de empleo.\nNo te desanimes, ya que cada oportunidad es una experiencia de aprendizaje. Te animamos a seguir buscando nuevas oportunidades y a perfeccionar tus habilidades y perfil profesional.\n¡Te deseamos mucho éxito en tus futuras búsquedas laborales!",
        }
    elif status == "4":
        return {
            "recipient": candidate,
            "verb": status_name,
            "description": f"¡Hola {candidate_name}!Queremos informarte que has sido aceptado para continuar en el proceso de contratación de la oferta '{candidature.offer.title}'. Esto significa que tu perfil ha sido seleccionado y ahora tendrás la oportunidad de participar en entrevistas y evaluaciones para demostrar tu capacidad y encaje con la empresa.\nTe recomendamos estar preparado(a) y atento(a) a las próximas etapas del proceso, ya que podrías recibir comunicaciones y solicitudes adicionales de {company}.\n¡Esperamos que tengas mucho éxito en esta fase de selección y puedas destacarte!",
        }
    elif status == "5":
        return {
            "recipient": candidate,
            "verb": status_name,
            "description": f"¡Felicitaciones {candidate_name}!\n¡Nos complace informarte que has sido contratado para la oferta {candidature.offer.title}! Después de superar todas las etapas del proceso de selección, has demostrado tu talento y encaje con [Nombre de la empresa]. ¡Bienvenido(a) al equipo!\nEstamos seguros de que serás un(a) valioso(a) miembro del equipo y contribuirás al éxito de la empresa. Esperamos que esta nueva oportunidad sea enriquecedora y te brinde crecimiento profesional.\n¡Te deseamos mucho éxito en esta nueva etapa de tu carrera!",
        }
    return None


def send_notification_of_candidacy_status(self):
    username = self.kwargs.get("username", "")
    p_status = self.request.GET.get("status", "")

    str_pk = get_pk_from_a_slug(self)
    candidate = User.objects.get(username=username)
    system_user = User.objects.get(username="system")
    candidature = self.model.objects.get(offer_id=str_pk, candidate=candidate)

    company_name = candidature.offer.user.username

    if hasattr(candidature.offer.user.userprofile, "company_profile"):
        company_name = candidature.offer.user.userprofile.company_profile.name

    message = get_message_to_state(
        status=p_status,
        candidature=candidature,
        candidate=candidate,
        company=company_name,
    )

    if message:
        notify.send(
            sender=system_user,
            recipient=message["recipient"],
            verb=message["verb"],
            target=candidature,
            description=message["description"],
        )
