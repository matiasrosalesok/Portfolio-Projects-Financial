import pandas as pd

def transformar_por_universidad(df: pd.DataFrame, universidad: str) -> pd.DataFrame:
    """
    Aplica transformaciones específicas según la universidad.
    Args:
        df: DataFrame con los datos a transformar.
        universidad: Código de la universidad ("UE", "UAX", "UAG", etc.)
    Returns:
        DataFrame transformado.
    """
    if universidad.upper() == "UE":
        # Ejemplo: agregar columna 'tags' solo para UE
         df["tags"] = "tags1,tags2"
    elif universidad.upper() == "UAX":
        # Para UAX no se agrega la columna 'tags'
        pass
    elif universidad.upper() == "UAG":
        # Puedes agregar otras transformaciones específicas para UAG aquí
        pass
    # Agrega más universidades y reglas si lo necesitas
    return df
