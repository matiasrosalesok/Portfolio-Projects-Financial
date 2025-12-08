import pandas as pd

def transformar_por_universidad(df: pd.DataFrame, financial_bank: str) -> pd.DataFrame:
    """
    Aplica transformaciones específicas según el entidad financiera.
    Args:
        df: DataFrame con los datos a transformar.
        entidad financiera: Código de la entidad financiera ("Bank_1", "Bank_2", "Bank_3", etc.)
    Returns:
        DataFrame transformado.
    """
    if financial_bank.upper() == "Bank_1":
        # Ejemplo: agregar columna 'tags' solo para Bank_1
         df["tags"] = "tags1,tags2"
    elif financial_bank.upper() == "Bank_2":
        # Para Bank_2 no se agrega la columna 'tags'
        pass
    elif financial_bank.upper() == "Bank_3":
        # Bank_1 agregar otras transformaciones específicas para Bank_3 aquí
        pass
    # Agrega más instuticiones financieras y reglas si lo necesitas
    return df
